import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def load_json(path_str: str):
    p = Path(path_str)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def bbox_to_box_args(bbox: dict):
    x = int(bbox.get("x", 0))
    y = int(bbox.get("y", 0))
    w = int(bbox.get("w", 0))
    h = int(bbox.get("h", 0))
    if w <= 0 or h <= 0:
        return None
    return [str(x), str(y), str(x + w), str(y + h)]


def run_inference(repo_dir: Path, inference_py: Path, inf_argv: list):
    launcher_code = (
        "import runpy,sys;"
        f"sys.path.insert(0,r'{str(repo_dir)}');"
        f"sys.argv={repr(inf_argv)};"
        f"runpy.run_path(r'{str(inference_py)}', run_name='__main__')"
    )
    cmd = [sys.executable, "-c", launcher_code]
    return subprocess.run(cmd, cwd=str(repo_dir), capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run official Wav2Lip inference with project metadata.")
    parser.add_argument("--video", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--target-json", required=True)
    parser.add_argument("--track-json", required=True)
    parser.add_argument("--timeline-json", required=True)

    parser.add_argument("--repo-dir", default=os.getenv("W2L_REPO_DIR", ""))
    parser.add_argument("--checkpoint", default=os.getenv("W2L_CHECKPOINT_PATH", ""))
    parser.add_argument("--face-det-batch", type=int, default=int(os.getenv("W2L_FACE_DET_BATCH", "16")))
    parser.add_argument("--wav2lip-batch", type=int, default=int(os.getenv("W2L_BATCH", "64")))
    parser.add_argument("--pads", default=os.getenv("W2L_PADS", "0 10 0 0"))
    parser.add_argument("--resize-factor", type=int, default=int(os.getenv("W2L_RESIZE_FACTOR", "1")))
    parser.add_argument("--nosmooth", action="store_true", default=os.getenv("W2L_NOSMOOTH", "0") == "1")
    parser.add_argument("--use-box", action="store_true", default=os.getenv("W2L_USE_BOX", "0") == "1")

    args = parser.parse_args()

    repo_dir = Path(args.repo_dir).resolve() if args.repo_dir else None
    checkpoint = Path(args.checkpoint).resolve() if args.checkpoint else None

    if repo_dir is None or not repo_dir.exists():
        print("ERROR: W2L_REPO_DIR is not configured or does not exist", file=sys.stderr)
        return 2
    inference_py = repo_dir / "inference.py"
    if not inference_py.exists():
        print(f"ERROR: inference.py not found in {repo_dir}", file=sys.stderr)
        return 2
    if checkpoint is None or not checkpoint.exists():
        print("ERROR: W2L_CHECKPOINT_PATH is not configured or does not exist", file=sys.stderr)
        return 2

    target = load_json(args.target_json)
    _track = load_json(args.track_json)
    _timeline = load_json(args.timeline_json)

    inf_argv = [
        "inference.py",
        "--checkpoint_path",
        str(checkpoint),
        "--face",
        str(Path(args.video).resolve()),
        "--audio",
        str(Path(args.audio).resolve()),
        "--outfile",
        str(Path(args.output).resolve()),
        "--face_det_batch_size",
        str(max(1, args.face_det_batch)),
        "--wav2lip_batch_size",
        str(max(1, args.wav2lip_batch)),
        "--resize_factor",
        str(max(1, args.resize_factor)),
    ]

    pads = [p for p in str(args.pads).split() if p.strip()]
    if len(pads) == 4:
        inf_argv.extend(["--pads", *pads])

    if args.nosmooth:
        inf_argv.append("--nosmooth")

    box_args = bbox_to_box_args((target or {}).get("bbox") or {})
    if args.use_box and box_args:
        inf_argv.extend(["--box", *box_args])

    proc = run_inference(repo_dir, inference_py, inf_argv)
    stderr_text = (proc.stderr or "").strip()
    if proc.returncode != 0 and "unexpected EOF" in stderr_text:
        alt_checkpoint = checkpoint.parent / "wav2lip.pth"
        if checkpoint.name.lower() == "wav2lip_gan.pth" and alt_checkpoint.exists():
            retry_argv = list(inf_argv)
            ckpt_idx = retry_argv.index("--checkpoint_path") + 1
            retry_argv[ckpt_idx] = str(alt_checkpoint.resolve())
            retry = run_inference(repo_dir, inference_py, retry_argv)
            if retry.returncode == 0:
                print("WARN: primary checkpoint failed with EOF; fallback checkpoint wav2lip.pth used")
                proc = retry
            else:
                proc = retry
    if proc.returncode != 0:
        stderr_out = (proc.stderr or "").strip()
        if "unexpected EOF" in stderr_out:
            hint = (
                f"Checkpoint file is corrupted or incomplete. "
                f"Re-download checkpoint and set W2L_CHECKPOINT_PATH. "
                f"Current path: {str(checkpoint)}"
            )
            if checkpoint.name.lower() == "wav2lip_gan.pth":
                alt_checkpoint = checkpoint.parent / "wav2lip.pth"
                hint += f"; fallback tried: {str(alt_checkpoint)}"
            stderr_out = f"{stderr_out}\n{hint}"
        sys.stderr.write(stderr_out + "\n")
        return proc.returncode

    out_path = Path(args.output)
    if not out_path.exists():
        print("ERROR: inference finished but output file not found", file=sys.stderr)
        return 3

    print("OK: Wav2Lip inference completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
