
const $ = (id) => document.getElementById(id);
const LAST_VIDEO_ID_KEY = "w2l_last_video_id";
const LANG_KEY = "w2l_lang";

const I18N = {
  en: {
    "title.sub": "Multi-face pipeline",
    "lang.label": "Lang",
    "window.min": "Minimize",
    "window.max": "Maximize",
    "window.close": "Close",
    "pipeline.title": "Pipeline",
    "pipeline.loading": "Pipeline mode: loading...",
    "step.runtime": "0. Runtime-настройки",
    "step.video": "1. Video",
    "step.face": "2. Face Selection",
    "step.track": "3. Smart Tracking целевого лица",
    "step.timeline": "4. Timeline (manual labeling)",
    "step.audio": "5. Audio and run",
    "runtime.exec_mode": "Режим выполнения",
    "runtime.core_open": "Core runtime settings",
    "runtime.timeout": "Таймаут (сек)",
    "runtime.command": "Шаблон команды",
    "runtime.command_ph": "python inference.py --face \"{video}\" --audio \"{audio}\" --outfile \"{output}\"",
    "runtime.checkpoint": "Путь к checkpoint",
    "runtime.checkpoint_ph": "C:\\path\\to\\wav2lip.pth",
    "runtime.use_box": "Use fixed box (--box)",
    "runtime.use_box_no": "No (auto detect each frame)",
    "runtime.use_box_yes": "Yes (fixed bbox from selected face)",
    "runtime.det_batch": "Face detector batch",
    "runtime.w2l_batch": "Wav2Lip batch",
    "runtime.pads": "Pads (top bottom left right)",
    "runtime.resize": "Resize factor",
    "runtime.nosmooth": "No smooth",
    "runtime.nosmooth_no": "No (smoother box trajectory)",
    "runtime.nosmooth_yes": "Yes (raw boxes, sharper but noisier)",
    "runtime.preset_label": "Preset",
    "runtime.preset_balanced": "Balanced quality",
    "runtime.preset_fast": "Fast preview",
    "runtime.preset_hq": "High quality stable",
    "runtime.preset_max": "Maximum quality",
    "runtime.preset_max_plus": "Maximum+ quality",
    "runtime.preset_apply": "Apply preset",
    "runtime.preset_balanced_desc": "Balanced: stable quality and moderate speed.",
    "runtime.preset_fast_desc": "Fast: quick iteration, lower quality and less stable tracking.",
    "runtime.preset_hq_desc": "High quality: cleaner lipsync, slower processing and higher GPU load.",
    "runtime.preset_max_desc": "Maximum: best quality stack with heavy post-processing.",
    "runtime.preset_max_plus_desc": "Maximum+: ultra-heavy quality mode with extreme postprocess and very slow render.",
    "runtime.enhance_open": "Enhancements",
    "runtime.enhance_title": "Quality Enhancements",
    "runtime.enhance_close": "Close",
    "runtime.enhance_save": "Save enhancements",
    "runtime.enhance_sharpen": "Sharpen mouth region",
    "runtime.enhance_sharpen_desc": "Improves mouth edge clarity; slightly increases render time.",
    "runtime.enhance_denoise": "Temporal denoise",
    "runtime.enhance_denoise_desc": "Reduces compression noise around lips and cheeks.",
    "runtime.enhance_color": "Color and contrast match",
    "runtime.enhance_color_desc": "Makes mouth blend more naturally with source frame colors.",
    "runtime.enhance_ultra": "Ultra postprocess (slow)",
    "runtime.enhance_ultra_desc": "Extra heavy detail/regrain pass for highest visual quality.",
    "runtime.enhance_extreme": "Extreme encode pass (very slow)",
    "runtime.enhance_extreme_desc": "Additional denoise/detail pass and ultra-slow encode for best final quality.",
    "runtime.enhance_face_restore": "ROI face restore",
    "runtime.enhance_face_restore_desc": "Restores and sharpens the target face region frame-by-frame.",
    "runtime.enhance_two_pass": "Two-pass postprocess",
    "runtime.enhance_two_pass_desc": "Runs an additional refinement pass for cleaner final details.",
    "runtime.enhance_quality_gate": "Quality gate rerender",
    "runtime.enhance_quality_gate_desc": "Checks output quality and automatically rerenders with stronger settings if needed.",
    "runtime.enhance_temporal": "Temporal consistency pass",
    "runtime.enhance_temporal_desc": "Adds extra temporal smoothing to reduce flicker across frames.",
    "runtime.enhance_deblock": "Deblock artifact cleanup",
    "runtime.enhance_deblock_desc": "Reduces compression blocks around mouth and jaw transitions.",
    "runtime.enhance_multicandidate": "Multi-candidate render",
    "runtime.enhance_multicandidate_desc": "Builds multiple heavy variants and keeps the best result.",
    "runtime.enhance_10bit": "10-bit intermediate pipeline",
    "runtime.enhance_10bit_desc": "Uses 10-bit intermediate encoding before final export to preserve gradients.",
    "runtime.enhance_anti_flicker": "Anti-flicker blend pass",
    "runtime.enhance_anti_flicker_desc": "Applies extra temporal blending to suppress residual flicker.",
    "runtime.enhance_scene_cut": "Scene-cut aware guard",
    "runtime.enhance_scene_cut_desc": "Auto-disables anti-flicker blending on high-cut videos to avoid ghosting on edits.",
    "runtime.enhance_summary_off": "Enhancements: off",
    "runtime.enhance_summary_on": "Enhancements enabled: {n}",
    "runtime.not_loaded": "Settings are not loaded.",
    "runtime.loaded": "Settings loaded.",
    "runtime.save": "Save settings",
    "runtime.placeholders": "Placeholders: {video} {audio} {output} {target_json} {track_json} {timeline_json} {project} {app}",
    "video.upload_label": "Upload source video",
    "video.upload_btn": "Upload video",
    "video.reset_btn": "Reset session",
    "video.not_selected": "Video is not selected.",
    "face.frame_pos": "Frame position",
    "face.probe_btn": "Show frame and faces",
    "face.not_selected": "Face is not selected.",
    "face.placeholder_no_video": "Upload video to preview frame",
    "track.step": "Sample step (frames)",
    "track.build_btn": "Build tracking",
    "track.not_built": "Tracking is not built.",
    "timeline.start": "Start (sec)",
    "timeline.end": "End (sec)",
    "timeline.speaker": "Speaker face_id",
    "timeline.add_btn": "Add segment",
    "timeline.save_btn": "Save timeline",
    "audio.upload_label": "Upload audio",
    "audio.submit_btn": "Create job",
    "jobs.title": "Jobs",
    "jobs.queue": "Queue: {n}",
    "jobs.refresh": "Refresh",
    "jobs.loading": "Loading...",
    "jobs.empty": "No jobs yet.",
    "jobs.progress": "Progress",
    "timeline.empty": "No segments added.",
    "timeline.delete": "Delete",
    "jobs.open_player": "Open in player",
    "jobs.download": "Download",
    "jobs.requeue": "Requeue",
    "jobs.cancel": "Cancel",
    "jobs.delete": "Delete",
    "session.reset_confirm": "Reset session?\nThis will clear restored video context and local form state.",
    "session.reset_selected": "Session reset. Select a video to continue.",
    "session.reset_done": "Session cleared.",
    "runtime.saved": "Saved: box={box}, det_batch={detBatch}, w2l_batch={w2lBatch}, pads=\"{pads}\"",
    "pipeline.mode": "Mode: {mode} | exec: {exec} | detector: {detector}",
    "pipeline.mode_command": "command (real inference)",
    "pipeline.mode_stub": "stub (copy mode)",
    "face.selected_fmt": "Selected face {id} (x:{x}, y:{y}, w:{w}, h:{h})",
    "track.ready_fmt": "Tracking ready: points={points}, coverage={coverage}%, step={step}",
    "jobs.created_meta": "Created: {created} | video: {video}",
    "jobs.target_face": "Target face: {faceId}",
    "jobs.open_failed": "Open output failed: {error}",
    "jobs.requeue_error": "Requeue error: {error}",
    "jobs.cancel_failed": "Cancel failed: {error}",
    "jobs.delete_failed": "Delete failed: {error}",
    "jobs.load_error": "Jobs load error: {error}",
    "config.error": "Config error: {error}",
    "settings.load_error": "Settings load error: {error}",
    "settings.save_error": "Settings save error: {error}",
    "probe.preview_loaded_click": "Preview loaded. Click face box to select target.",
    "probe.preview_loaded_none": "Preview loaded. No faces found near first frame.",
    "video.select_file": "Select a video file.",
    "video.uploading": "Uploading video...",
    "probe.error": "Probe error: {error}",
    "video.uploaded": "Video uploaded. video_id={videoId}{meta}",
    "video.upload_error": "Video upload error: {error}",
    "video.restored": "Restored video_id={videoId}{meta}",
    "video.restore_unavailable": "Saved video context is unavailable: {error}",
    "video.upload_first": "Upload video first.",
    "face.detecting": "Detecting faces...",
    "face.click_select": "Click face box to select target.",
    "face.none_found_retry": "No faces found. Move slider and retry.",
    "face.updated_rebuild": "Face updated, rebuild tracking.",
    "face.select_first": "Select target face first.",
    "face.selection_error": "Face selection error: {error}",
    "track.building": "Building tracking...",
    "track.error": "Tracking error: {error}",
    "timeline.invalid_segment": "Invalid segment: end must be greater than start.",
    "timeline.saved": "Timeline saved: {saved}/{input}, dropped={dropped}, overlap_adjusted={overlap}, merged={merged}, max={max}",
    "timeline.save_error": "Timeline save error: {error}",
    "audio.select_file": "Select an audio file.",
    "job.submit_build_tracking": "Build target-face tracking first.",
    "job.submitting": "Submitting job...",
    "job.created": "Job created: {jobId}",
    "job.submit_error": "Submit error: {error}"
  },
  ru: {
    "title.sub": "\u041f\u0430\u0439\u043f\u043b\u0430\u0439\u043d \u0434\u043b\u044f \u043c\u043d\u043e\u0433\u0438\u0445 \u043b\u0438\u0446",
    "lang.label": "\u042f\u0437\u044b\u043a",
    "window.min": "\u0421\u0432\u0435\u0440\u043d\u0443\u0442\u044c",
    "window.max": "\u0420\u0430\u0437\u0432\u0435\u0440\u043d\u0443\u0442\u044c",
    "window.close": "\u0417\u0430\u043a\u0440\u044b\u0442\u044c",
    "pipeline.title": "\u041f\u0430\u0439\u043f\u043b\u0430\u0439\u043d",
    "pipeline.loading": "\u0420\u0435\u0436\u0438\u043c \u043f\u0430\u0439\u043f\u043b\u0430\u0439\u043d\u0430: \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0430...",
    "step.runtime": "0. Runtime Settings",
    "step.video": "1. \u0412\u0438\u0434\u0435\u043e",
    "step.face": "2. \u0412\u044b\u0431\u043e\u0440 \u043b\u0438\u0446\u0430",
    "step.track": "3. Smart Tracking target-face",
    "step.timeline": "4. \u0422\u0430\u0439\u043c\u043b\u0430\u0439\u043d (\u0440\u0443\u0447\u043d\u0430\u044f \u0440\u0430\u0437\u043c\u0435\u0442\u043a\u0430)",
    "step.audio": "5. \u0410\u0443\u0434\u0438\u043e \u0438 \u0437\u0430\u043f\u0443\u0441\u043a",
    "runtime.exec_mode": "Exec mode",
    "runtime.core_open": "\u0411\u0430\u0437\u043e\u0432\u044b\u0435 runtime-\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438",
    "runtime.timeout": "Timeout sec",
    "runtime.command": "Command template",
    "runtime.command_ph": "python inference.py --face \"{video}\" --audio \"{audio}\" --outfile \"{output}\"",
    "runtime.checkpoint": "Checkpoint path",
    "runtime.checkpoint_ph": "C:\\path\\to\\wav2lip.pth",
    "runtime.use_box": "\u0424\u0438\u043a\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 box (--box)",
    "runtime.use_box_no": "\u041d\u0435\u0442 (\u0430\u0432\u0442\u043e\u0434\u0435\u0442\u0435\u043a\u0442 \u043a\u0430\u0436\u0434\u043e\u0433\u043e \u043a\u0430\u0434\u0440\u0430)",
    "runtime.use_box_yes": "\u0414\u0430 (\u0444\u0438\u043a\u0441 \u043f\u043e \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u043c\u0443 \u043b\u0438\u0446\u0443)",
    "runtime.det_batch": "\u0411\u0430\u0442\u0447 \u0434\u0435\u0442\u0435\u043a\u0442\u043e\u0440\u0430 \u043b\u0438\u0446",
    "runtime.w2l_batch": "\u0411\u0430\u0442\u0447 Wav2Lip",
    "runtime.pads": "Отступы (верх низ лево право)",
    "runtime.resize": "Коэффициент resize",
    "runtime.nosmooth": "Без сглаживания",
    "runtime.nosmooth_no": "\u041d\u0435\u0442 (\u0431\u043e\u043b\u0435\u0435 \u043f\u043b\u0430\u0432\u043d\u043e)",
    "runtime.nosmooth_yes": "\u0414\u0430 (\u0431\u043e\u043b\u0435\u0435 \u0440\u0435\u0437\u043a\u043e)",
    "runtime.preset_label": "\u041f\u0440\u0435\u0441\u0435\u0442",
    "runtime.preset_balanced": "\u0421\u0431\u0430\u043b\u0430\u043d\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439",
    "runtime.preset_fast": "\u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u043f\u0440\u0435\u0432\u044c\u044e",
    "runtime.preset_hq": "\u0412\u044b\u0441\u043e\u043a\u043e\u0435 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u043e",
    "runtime.preset_max": "\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430",
    "runtime.preset_max_plus": "\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c+ \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430",
    "runtime.preset_apply": "\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c \u043f\u0440\u0435\u0441\u0435\u0442",
    "runtime.preset_balanced_desc": "\u0421\u0431\u0430\u043b\u0430\u043d\u0441: \u0441\u0442\u0430\u0431\u0438\u043b\u044c\u043d\u043e\u0435 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u043e \u0438 \u0443\u043c\u0435\u0440\u0435\u043d\u043d\u0430\u044f \u0441\u043a\u043e\u0440\u043e\u0441\u0442\u044c.",
    "runtime.preset_fast_desc": "\u0411\u044b\u0441\u0442\u0440\u043e: \u043c\u0430\u043a\u0441\u0438\u043c\u0443\u043c \u0441\u043a\u043e\u0440\u043e\u0441\u0442\u0438 \u0434\u043b\u044f \u043f\u0440\u043e\u0431, \u043d\u043e \u043d\u0438\u0436\u0435 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u043e/\u0441\u0442\u0430\u0431\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u044c.",
    "runtime.preset_hq_desc": "\u0412\u044b\u0441\u043e\u043a\u043e\u0435 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u043e: \u043b\u0443\u0447\u0448\u0435 \u0432\u0438\u0434\u0438\u043c\u044b\u0439 lipsync, \u043d\u043e \u0434\u043e\u043b\u044c\u0448\u0435 \u0438 \u0442\u044f\u0436\u0435\u043b\u0435\u0435 \u0434\u043b\u044f GPU.",
    "runtime.preset_max_desc": "\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c: \u043f\u0438\u043a\u043e\u0432\u043e\u0435 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u043e \u0441 \u0442\u044f\u0436\u0435\u043b\u044b\u043c post-processing.",
    "runtime.preset_max_plus_desc": "\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c+: \u0443\u043b\u044c\u0442\u0440\u0430-\u0442\u044f\u0436\u0435\u043b\u044b\u0439 \u0440\u0435\u0436\u0438\u043c \u0441 extreme postprocess \u0438 \u043e\u0447\u0435\u043d\u044c \u043c\u0435\u0434\u043b\u0435\u043d\u043d\u044b\u043c \u0440\u0435\u043d\u0434\u0435\u0440\u043e\u043c.",
    "runtime.enhance_open": "\u0423\u043b\u0443\u0447\u0448\u0430\u043b\u043a\u0438",
    "runtime.enhance_title": "\u0423\u043b\u0443\u0447\u0448\u0435\u043d\u0438\u044f \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430",
    "runtime.enhance_close": "\u0417\u0430\u043a\u0440\u044b\u0442\u044c",
    "runtime.enhance_save": "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0443\u043b\u0443\u0447\u0448\u0430\u043b\u043a\u0438",
    "runtime.enhance_sharpen": "\u0420\u0435\u0437\u043a\u043e\u0441\u0442\u044c \u0437\u043e\u043d\u044b \u0440\u0442\u0430",
    "runtime.enhance_sharpen_desc": "\u0414\u0435\u043b\u0430\u0435\u0442 \u043a\u0440\u0430\u044f \u0433\u0443\u0431 \u0447\u0438\u0449\u0435; \u0441\u043b\u0435\u0433\u043a\u0430 \u0437\u0430\u043c\u0435\u0434\u043b\u044f\u0435\u0442 \u0440\u0435\u043d\u0434\u0435\u0440.",
    "runtime.enhance_denoise": "\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439 denoise",
    "runtime.enhance_denoise_desc": "\u0423\u043c\u0435\u043d\u044c\u0448\u0430\u0435\u0442 \u0448\u0443\u043c/\u0431\u043b\u043e\u043a\u0438 \u0432\u043e\u043a\u0440\u0443\u0433 \u0433\u0443\u0431 \u0438 \u0449\u0435\u043a.",
    "runtime.enhance_color": "\u0421\u0432\u0435\u0442/\u0446\u0432\u0435\u0442 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u044f",
    "runtime.enhance_color_desc": "\u0414\u0435\u043b\u0430\u0435\u0442 \u0432\u0448\u0438\u0432\u043a\u0443 \u0440\u0442\u0430 \u0431\u043e\u043b\u0435\u0435 \u0435\u0441\u0442\u0435\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0439 \u043f\u043e \u0442\u043e\u043d\u0443.",
    "runtime.enhance_ultra": "Ultra postprocess (\u043c\u0435\u0434\u043b\u0435\u043d\u043d\u043e)",
    "runtime.enhance_ultra_desc": "\u0422\u044f\u0436\u0435\u043b\u044b\u0439 \u0434\u0435\u0442\u0430\u043b\u044c\u043d\u044b\u0439 pass \u0434\u043b\u044f \u043c\u0430\u043a\u0441\u0438\u043c\u0443\u043c\u0430 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430.",
    "runtime.enhance_extreme": "Extreme encode pass (\u043e\u0447\u0435\u043d\u044c \u043c\u0435\u0434\u043b\u0435\u043d\u043d\u043e)",
    "runtime.enhance_extreme_desc": "\u0414\u043e\u043f. \u0434\u0435\u0442\u0430\u043b\u044c\u043d\u044b\u0439/denoise pass \u0438 \u0441\u0432\u0435\u0440\u0445\u043c\u0435\u0434\u043b\u0435\u043d\u043d\u044b\u0439 encode \u0434\u043b\u044f \u043f\u0438\u043a\u0430 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0430.",
    "runtime.enhance_face_restore": "ROI face restore",
    "runtime.enhance_face_restore_desc": "\u041f\u043e\u043a\u0430\u0434\u0440\u043e\u0432\u043e \u0432\u043e\u0441\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442/\u0443\u0441\u0438\u043b\u0438\u0432\u0430\u0435\u0442 \u0437\u043e\u043d\u0443 \u0446\u0435\u043b\u0435\u0432\u043e\u0433\u043e \u043b\u0438\u0446\u0430.",
    "runtime.enhance_two_pass": "\u0414\u0432\u0443\u0445\u043f\u0440\u043e\u0445\u043e\u0434\u043d\u044b\u0439 postprocess",
    "runtime.enhance_two_pass_desc": "\u0414\u0435\u043b\u0430\u0435\u0442 \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442. pass \u0434\u043b\u044f \u0447\u0438\u0441\u0442\u044b\u0445 \u043c\u0435\u043b\u043a\u0438\u0445 \u0434\u0435\u0442\u0430\u043b\u0435\u0439.",
    "runtime.enhance_quality_gate": "Quality gate rerender",
    "runtime.enhance_quality_gate_desc": "\u041e\u0446\u0435\u043d\u0438\u0432\u0430\u0435\u0442 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u043e \u0438 \u0430\u0432\u0442\u043e-\u043f\u0435\u0440\u0435\u0440\u0435\u043d\u0434\u0435\u0440\u0438\u0442 \u0432 \u0443\u0441\u0438\u043b\u0435\u043d\u043d\u043e\u043c \u0440\u0435\u0436\u0438\u043c\u0435.",
    "runtime.enhance_temporal": "Temporal consistency pass",
    "runtime.enhance_temporal_desc": "\u0414\u043e\u043f. \u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0435 \u0441\u0433\u043b\u0430\u0436\u0438\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0443\u043c\u0435\u043d\u044c\u0448\u0435\u043d\u0438\u044f \u0444\u043b\u0438\u043a\u0435\u0440\u0430.",
    "runtime.enhance_deblock": "Deblock artifact cleanup",
    "runtime.enhance_deblock_desc": "\u0423\u043c\u0435\u043d\u044c\u0448\u0430\u0435\u0442 \u0431\u043b\u043e\u0447\u043d\u044b\u0435 \u0430\u0440\u0442\u0435\u0444\u0430\u043a\u0442\u044b \u0432 \u0437\u043e\u043d\u0435 \u0440\u0442\u0430/\u0447\u0435\u043b\u044e\u0441\u0442\u0438.",
    "runtime.enhance_multicandidate": "Multi-candidate render",
    "runtime.enhance_multicandidate_desc": "\u0421\u0442\u0440\u043e\u0438\u0442 \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e heavy-\u0432\u0430\u0440\u0438\u0430\u043d\u0442\u043e\u0432 \u0438 \u043e\u0441\u0442\u0430\u0432\u043b\u044f\u0435\u0442 \u043b\u0443\u0447\u0448\u0438\u0439.",
    "runtime.enhance_10bit": "10-bit intermediate pipeline",
    "runtime.enhance_10bit_desc": "10-bit \u043f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u0447\u043d\u044b\u0439 pipeline \u0434\u043b\u044f \u043b\u0443\u0447\u0448\u0438\u0445 \u0433\u0440\u0430\u0434\u0438\u0435\u043d\u0442\u043e\u0432.",
    "runtime.enhance_anti_flicker": "Anti-flicker blend pass",
    "runtime.enhance_anti_flicker_desc": "\u0414\u043e\u043f. temporal blend-pass \u0434\u043b\u044f \u043f\u043e\u0434\u0430\u0432\u043b\u0435\u043d\u0438\u044f \u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e\u0433\u043e \u0444\u043b\u0438\u043a\u0435\u0440\u0430.",
    "runtime.enhance_scene_cut": "Scene-cut aware guard",
    "runtime.enhance_scene_cut_desc": "\u0410\u0432\u0442\u043e-\u043e\u0442\u043a\u043b\u044e\u0447\u0430\u0435\u0442 anti-flicker \u043d\u0430 \u0432\u0438\u0434\u0435\u043e \u0441 \u0447\u0430\u0441\u0442\u044b\u043c\u0438 \u0441\u043a\u043b\u0435\u0439\u043a\u0430\u043c\u0438, \u0447\u0442\u043e\u0431\u044b \u0438\u0437\u0431\u0435\u0436\u0430\u0442\u044c ghosting.",
    "runtime.enhance_summary_off": "\u0423\u043b\u0443\u0447\u0448\u0430\u043b\u043a\u0438: \u0432\u044b\u043a\u043b",
    "runtime.enhance_summary_on": "\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u043e \u0443\u043b\u0443\u0447\u0448\u0430\u043b\u043e\u043a: {n}",
    "runtime.not_loaded": "\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043d\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u044b.",
    "runtime.loaded": "\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u044b.",
    "runtime.save": "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c настройки",
    "runtime.placeholders": "\u041f\u043b\u0435\u0439\u0441\u0445\u043e\u043b\u0434\u0435\u0440\u044b: {video} {audio} {output} {target_json} {track_json} {timeline_json} {project} {app}",
    "video.upload_label": "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u0435 \u0438\u0441\u0445\u043e\u0434\u043d\u043e\u0435 \u0432\u0438\u0434\u0435\u043e",
    "video.upload_btn": "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0432\u0438\u0434\u0435\u043e",
    "video.reset_btn": "\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u0441\u0435\u0441\u0441\u0438\u044e",
    "video.not_selected": "\u0412\u0438\u0434\u0435\u043e \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u043e.",
    "face.frame_pos": "\u041f\u043e\u0437\u0438\u0446\u0438\u044f \u043a\u0430\u0434\u0440\u0430",
    "face.probe_btn": "\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u043a\u0430\u0434\u0440 \u0438 \u043b\u0438\u0446\u0430",
    "face.not_selected": "\u041b\u0438\u0446\u043e \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u043e.",
    "face.placeholder_no_video": "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u0435 \u0432\u0438\u0434\u0435\u043e, \u0447\u0442\u043e\u0431\u044b \u0443\u0432\u0438\u0434\u0435\u0442\u044c \u043a\u0430\u0434\u0440",
    "track.step": "Шаг семплирования (кадры)",
    "track.build_btn": "\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0442\u0440\u0435\u043a\u0438\u043d\u0433",
    "track.not_built": "\u0422\u0440\u0435\u043a\u0438\u043d\u0433 \u043d\u0435 \u043f\u043e\u0441\u0442\u0440\u043e\u0435\u043d.",
    "timeline.start": "Начало (сек)",
    "timeline.end": "Конец (сек)",
    "timeline.speaker": "face_id говорящего",
    "timeline.add_btn": "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0435\u0433\u043c\u0435\u043d\u0442",
    "timeline.save_btn": "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0442\u0430\u0439\u043c\u043b\u0430\u0439\u043d",
    "audio.upload_label": "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u0435 \u0430\u0443\u0434\u0438\u043e",
    "audio.submit_btn": "\u0421\u043e\u0437\u0434\u0430\u0442\u044c задачу",
    "jobs.title": "Задачи",
    "jobs.queue": "\u041e\u0447\u0435\u0440\u0435\u0434\u044c: {n}",
    "jobs.refresh": "\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c",
    "jobs.loading": "\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430...",
    "jobs.empty": "\u041f\u043e\u043a\u0430 \u043d\u0435\u0442 задач.",
    "jobs.progress": "\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441",
    "timeline.empty": "\u0421\u0435\u0433\u043c\u0435\u043d\u0442\u044b \u043d\u0435 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u044b.",
    "timeline.delete": "\u0423\u0434\u0430\u043b\u0438\u0442\u044c",
    "jobs.open_player": "\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u043f\u043b\u0435\u0435\u0440\u0435",
    "jobs.download": "\u0421\u043a\u0430\u0447\u0430\u0442\u044c",
    "jobs.requeue": "\u041f\u043e\u0432\u0442\u043e\u0440\u0438\u0442\u044c",
    "jobs.cancel": "\u041e\u0442\u043c\u0435\u043d\u0430",
    "jobs.delete": "\u0423\u0434\u0430\u043b\u0438\u0442\u044c",
    "session.reset_confirm": "\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u0441\u0435\u0441\u0441\u0438\u044e?\n\u0411\u0443\u0434\u0435\u0442 \u043e\u0447\u0438\u0449\u0435\u043d \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442 \u0438 \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u0444\u043e\u0440\u043c.",
    "session.reset_selected": "\u0421\u0435\u0441\u0441\u0438\u044f \u0441\u0431\u0440\u043e\u0448\u0435\u043d\u0430. \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0432\u0438\u0434\u0435\u043e.",
    "session.reset_done": "\u0421\u0435\u0441\u0441\u0438\u044f \u043e\u0447\u0438\u0449\u0435\u043d\u0430.",
    "runtime.saved": "\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u043e: box={box}, det_batch={detBatch}, w2l_batch={w2lBatch}, pads=\"{pads}\"",
    "pipeline.mode": "\u0420\u0435\u0436\u0438\u043c: {mode} | exec: {exec} | detector: {detector}",
    "pipeline.mode_command": "command (\u0440\u0435\u0430\u043b\u044c\u043d\u044b\u0439 inference)",
    "pipeline.mode_stub": "stub (\u0437\u0430\u0433\u043b\u0443\u0448\u043a\u0430)",
    "face.selected_fmt": "\u0412\u044b\u0431\u0440\u0430\u043d\u043e \u043b\u0438\u0446\u043e {id} (x:{x}, y:{y}, w:{w}, h:{h})",
    "track.ready_fmt": "\u0422\u0440\u0435\u043a\u0438\u043d\u0433 \u0433\u043e\u0442\u043e\u0432: points={points}, coverage={coverage}%, step={step}",
    "jobs.created_meta": "\u0421\u043e\u0437\u0434\u0430\u043d\u043e: {created} | \u0432\u0438\u0434\u0435\u043e: {video}",
    "jobs.target_face": "\u0426\u0435\u043b\u0435\u0432\u043e\u0435 \u043b\u0438\u0446\u043e: {faceId}",
    "jobs.open_failed": "\u041e\u0448\u0438\u0431\u043a\u0430 \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u044f \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430: {error}",
    "jobs.requeue_error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u043e\u0432\u0442\u043e\u0440\u043d\u043e\u0439 \u043f\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438: {error}",
    "jobs.cancel_failed": "\u041e\u0448\u0438\u0431\u043a\u0430 \u043e\u0442\u043c\u0435\u043d\u044b: {error}",
    "jobs.delete_failed": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f: {error}",
    "jobs.load_error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438 jobs: {error}",
    "config.error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u043a\u043e\u043d\u0444\u0438\u0433\u0430: {error}",
    "settings.load_error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438 settings: {error}",
    "settings.save_error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f settings: {error}",
    "probe.preview_loaded_click": "\u041f\u0440\u0435\u0432\u044c\u044e \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043e. \u041a\u043b\u0438\u043a\u043d\u0438\u0442\u0435 \u043f\u043e \u0440\u0430\u043c\u043a\u0435 \u043b\u0438\u0446\u0430 \u0434\u043b\u044f \u0432\u044b\u0431\u043e\u0440\u0430.",
    "probe.preview_loaded_none": "\u041f\u0440\u0435\u0432\u044c\u044e \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043e. \u041b\u0438\u0446 \u0440\u044f\u0434\u043e\u043c \u0441 \u043f\u0435\u0440\u0432\u044b\u043c \u043a\u0430\u0434\u0440\u043e\u043c \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e.",
    "video.select_file": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0432\u0438\u0434\u0435\u043e\u0444\u0430\u0439\u043b.",
    "video.uploading": "\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0432\u0438\u0434\u0435\u043e...",
    "probe.error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u0440\u043e\u0431\u044b: {error}",
    "video.uploaded": "\u0412\u0438\u0434\u0435\u043e \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043e. video_id={videoId}{meta}",
    "video.upload_error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438 \u0432\u0438\u0434\u0435\u043e: {error}",
    "video.restored": "\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d video_id={videoId}{meta}",
    "video.restore_unavailable": "\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442 \u0432\u0438\u0434\u0435\u043e \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d: {error}",
    "video.upload_first": "\u0421\u043d\u0430\u0447\u0430\u043b\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u0435 \u0432\u0438\u0434\u0435\u043e.",
    "face.detecting": "\u041f\u043e\u0438\u0441\u043a \u043b\u0438\u0446...",
    "face.click_select": "\u041a\u043b\u0438\u043a\u043d\u0438\u0442\u0435 \u043f\u043e \u0440\u0430\u043c\u043a\u0435 \u043b\u0438\u0446\u0430 \u0434\u043b\u044f \u0432\u044b\u0431\u043e\u0440\u0430.",
    "face.none_found_retry": "\u041b\u0438\u0446\u0430 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u044b. \u0421\u0434\u0432\u0438\u043d\u044c\u0442\u0435 \u0441\u043b\u0430\u0439\u0434\u0435\u0440 \u0438 \u043f\u043e\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u0441\u043d\u043e\u0432\u0430.",
    "face.updated_rebuild": "\u041b\u0438\u0446\u043e \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u043e, \u043f\u0435\u0440\u0435\u0441\u043e\u0431\u0435\u0440\u0438\u0442\u0435 \u0442\u0440\u0435\u043a\u0438\u043d\u0433.",
    "face.select_first": "\u0421\u043d\u0430\u0447\u0430\u043b\u0430 \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0446\u0435\u043b\u0435\u0432\u043e\u0435 \u043b\u0438\u0446\u043e.",
    "face.selection_error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0432\u044b\u0431\u043e\u0440\u0430 \u043b\u0438\u0446\u0430: {error}",
    "track.building": "\u0421\u0431\u043e\u0440\u043a\u0430 \u0442\u0440\u0435\u043a\u0438\u043d\u0433\u0430...",
    "track.error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0442\u0440\u0435\u043a\u0438\u043d\u0433\u0430: {error}",
    "timeline.invalid_segment": "\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u0441\u0435\u0433\u043c\u0435\u043d\u0442: end \u0434\u043e\u043b\u0436\u0435\u043d \u0431\u044b\u0442\u044c \u0431\u043e\u043b\u044c\u0448\u0435 start.",
    "timeline.saved": "\u0422\u0430\u0439\u043c\u043b\u0430\u0439\u043d \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d: {saved}/{input}, dropped={dropped}, overlap_adjusted={overlap}, merged={merged}, max={max}",
    "timeline.save_error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f \u0442\u0430\u0439\u043c\u043b\u0430\u0439\u043d\u0430: {error}",
    "audio.select_file": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0430\u0443\u0434\u0438\u043e\u0444\u0430\u0439\u043b.",
    "job.submit_build_tracking": "\u0421\u043d\u0430\u0447\u0430\u043b\u0430 \u043f\u043e\u0441\u0442\u0440\u043e\u0439\u0442\u0435 \u0442\u0440\u0435\u043a\u0438\u043d\u0433 target-face.",
    "job.submitting": "\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 job...",
    "job.created": "Job \u0441\u043e\u0437\u0434\u0430\u043d: {jobId}",
    "job.submit_error": "\u041e\u0448\u0438\u0431\u043a\u0430 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438: {error}"
  }
};

const state = {
  dragging: false,
  dragOffsetX: 0,
  dragOffsetY: 0,
  pollTimer: 0,
  videoId: "",
  detectorMode: "",
  probe: null,
  selectedFace: null,
  tracking: null,
  timelineSegments: [],
  videoMeta: null,
  lang: "en",
  probeDebounce: 0,
  jobsFingerprint: "",
};

const RUNTIME_PRESETS = {
  balanced: {
    use_box: "0", face_det_batch: 16, wav2lip_batch: 64, pads: "0 10 0 0", resize_factor: 1, nosmooth: "0",
    enhance_sharpen: false, enhance_denoise: false, enhance_color_boost: false, enhance_ultra: false, enhance_extreme: false,
    enhance_face_restore: false, enhance_two_pass: false, enhance_quality_gate: false, enhance_temporal: false,
    enhance_deblock: false, enhance_multicandidate: false, enhance_10bit: false, enhance_anti_flicker: false, enhance_scene_cut: false,
  },
  fast: {
    use_box: "0", face_det_batch: 8, wav2lip_batch: 96, pads: "0 12 0 0", resize_factor: 2, nosmooth: "1",
    enhance_sharpen: false, enhance_denoise: false, enhance_color_boost: false, enhance_ultra: false, enhance_extreme: false,
    enhance_face_restore: false, enhance_two_pass: false, enhance_quality_gate: false, enhance_temporal: false,
    enhance_deblock: false, enhance_multicandidate: false, enhance_10bit: false, enhance_anti_flicker: false, enhance_scene_cut: false,
  },
  hq: {
    use_box: "0", face_det_batch: 4, wav2lip_batch: 24, pads: "0 6 0 0", resize_factor: 1, nosmooth: "0",
    enhance_sharpen: true, enhance_denoise: false, enhance_color_boost: true, enhance_ultra: false, enhance_extreme: false,
    enhance_face_restore: true, enhance_two_pass: false, enhance_quality_gate: false, enhance_temporal: false,
    enhance_deblock: true, enhance_multicandidate: false, enhance_10bit: false, enhance_anti_flicker: false, enhance_scene_cut: false,
  },
  max: {
    use_box: "0", face_det_batch: 2, wav2lip_batch: 8, pads: "0 6 0 0", resize_factor: 1, nosmooth: "0",
    enhance_sharpen: true, enhance_denoise: true, enhance_color_boost: true, enhance_ultra: true, enhance_extreme: false,
    enhance_face_restore: true, enhance_two_pass: true, enhance_quality_gate: true, enhance_temporal: true,
    enhance_deblock: true, enhance_multicandidate: true, enhance_10bit: true, enhance_anti_flicker: true, enhance_scene_cut: true,
  },
  max_plus: {
    use_box: "0", face_det_batch: 1, wav2lip_batch: 4, pads: "0 6 0 0", resize_factor: 1, nosmooth: "0",
    enhance_sharpen: true, enhance_denoise: true, enhance_color_boost: true, enhance_ultra: true, enhance_extreme: true,
    enhance_face_restore: true, enhance_two_pass: true, enhance_quality_gate: true, enhance_temporal: true,
    enhance_deblock: true, enhance_multicandidate: true, enhance_10bit: true, enhance_anti_flicker: true, enhance_scene_cut: true,
  },
};

function jobsFingerprint(jobs) {
  if (!Array.isArray(jobs)) return "";
  return JSON.stringify(
    jobs.map((j) => [
      String(j && j.id || ""),
      String(j && j.status || ""),
      Number(j && j.progress || 0),
      String(j && j.message || ""),
      String(j && j.updated_at || ""),
      String(j && j.output_url || ""),
    ])
  );
}

function t(key, vars = {}) {
  const dict = I18N[state.lang] || I18N.en;
  const base = dict[key] || I18N.en[key] || key;
  return String(base).replace(/\{(\w+)\}/g, (_, name) => {
    if (Object.prototype.hasOwnProperty.call(vars, name) && vars[name] !== null && vars[name] !== undefined) {
      return String(vars[name]);
    }
    return `{${name}}`;
  });
}

function loadLang() {
  try {
    const v = String(localStorage.getItem(LANG_KEY) || "").trim().toLowerCase();
    if (v === "ru" || v === "en") return v;
  } catch (_) {}
  return "en";
}

function saveLang(lang) {
  try {
    localStorage.setItem(LANG_KEY, lang);
  } catch (_) {}
}

function applyStaticI18n() {
  document.documentElement.lang = state.lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (key) el.textContent = t(key);
  });
  document.querySelectorAll("[data-i18n-title]").forEach((el) => {
    const key = el.getAttribute("data-i18n-title");
    if (key) el.title = t(key);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (key) el.setAttribute("placeholder", t(key));
  });
}

function setLanguage(lang) {
  state.lang = lang === "ru" ? "ru" : "en";
  saveLang(state.lang);
  const sel = $("langSelect");
  if (sel) sel.value = state.lang;
  applyStaticI18n();
  updatePresetInfo();
  updateEnhanceSummary();
  renderTimeline();
  refreshConfig();
  refreshJobs();
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}

async function windowAction(action) {
  try {
    await api("/api/window/action", { method: "POST", body: JSON.stringify({ action }) });
  } catch (_) {
    if (action === "close") {
      try {
        window.close();
      } catch (_) {}
    }
  }
}

function fmtTime(iso) {
  if (!iso) return "-";
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? iso : d.toLocaleString();
}

function fmtSeconds(sec) {
  const n = Number(sec);
  if (!Number.isFinite(n) || n <= 0) return "-";
  return `${n.toFixed(2)}s`;
}

function videoEndSec(meta) {
  if (!meta) return null;
  const fps = Number(meta.fps);
  const frameCount = Number(meta.frame_count);
  if (Number.isFinite(fps) && fps > 0 && Number.isFinite(frameCount) && frameCount > 1) {
    return (frameCount - 1) / fps;
  }
  const duration = Number(meta.duration_sec);
  if (Number.isFinite(duration) && duration > 0) return duration;
  return null;
}

function clampPercent(value) {
  const num = Number(value);
  if (!Number.isFinite(num)) return 0;
  return Math.max(0, Math.min(100, Math.round(num)));
}

function estimateJobProgress(job) {
  const explicit = clampPercent(job && job.progress);
  if (Number.isFinite(Number(job && job.progress))) return explicit;
  const s = String((job && job.status) || "").toLowerCase();
  if (s === "done") return 100;
  if (s === "failed" || s === "canceled") return 100;
  if (s === "running") return 55;
  if (s === "leased") return 10;
  if (s === "queued") return 5;
  return 0;
}

function fmtVideoMeta(meta) {
  if (!meta) return "";
  const w = Number(meta.width);
  const h = Number(meta.height);
  const fps = Number(meta.fps);
  const frameCount = Number(meta.frame_count);
  const duration = Number(meta.duration_sec);
  const parts = [];
  if (Number.isFinite(w) && Number.isFinite(h) && w > 0 && h > 0) parts.push(`${w}x${h}`);
  if (Number.isFinite(fps) && fps > 0) parts.push(`fps=${fps.toFixed(2)}`);
  if (Number.isFinite(frameCount) && frameCount > 0) parts.push(`frames=${Math.round(frameCount)}`);
  if (Number.isFinite(duration) && duration > 0) parts.push(`duration=${duration.toFixed(2)}s`);
  return parts.length ? ` | ${parts.join(" | ")}` : "";
}

function setTimelineEndFromVideoMeta() {
  const endSec = videoEndSec(state.videoMeta);
  if (!(endSec > 0)) return;
  const endRounded = Math.max(0.01, Math.round(endSec * 1000) / 1000);
  $("segStart").value = "0";
  $("segEnd").value = String(endRounded);
}

function presetDescKey(name) {
  if (name === "fast") return "runtime.preset_fast_desc";
  if (name === "hq") return "runtime.preset_hq_desc";
  if (name === "max") return "runtime.preset_max_desc";
  if (name === "max_plus") return "runtime.preset_max_plus_desc";
  return "runtime.preset_balanced_desc";
}

function readEnhancements() {
  return {
    enhance_sharpen: !!($("enhanceSharpen") && $("enhanceSharpen").checked),
    enhance_denoise: !!($("enhanceDenoise") && $("enhanceDenoise").checked),
    enhance_color_boost: !!($("enhanceColorBoost") && $("enhanceColorBoost").checked),
    enhance_ultra: !!($("enhanceUltra") && $("enhanceUltra").checked),
    enhance_extreme: !!($("enhanceExtreme") && $("enhanceExtreme").checked),
    enhance_face_restore: !!($("enhanceFaceRestore") && $("enhanceFaceRestore").checked),
    enhance_two_pass: !!($("enhanceTwoPass") && $("enhanceTwoPass").checked),
    enhance_quality_gate: !!($("enhanceQualityGate") && $("enhanceQualityGate").checked),
    enhance_temporal: !!($("enhanceTemporal") && $("enhanceTemporal").checked),
    enhance_deblock: !!($("enhanceDeblock") && $("enhanceDeblock").checked),
    enhance_multicandidate: !!($("enhanceMultiCandidate") && $("enhanceMultiCandidate").checked),
    enhance_10bit: !!($("enhance10bit") && $("enhance10bit").checked),
    enhance_anti_flicker: !!($("enhanceAntiFlicker") && $("enhanceAntiFlicker").checked),
    enhance_scene_cut: !!($("enhanceSceneCut") && $("enhanceSceneCut").checked),
  };
}

function applyEnhancementsFlags(flags) {
  if ($("enhanceSharpen")) $("enhanceSharpen").checked = !!flags.enhance_sharpen;
  if ($("enhanceDenoise")) $("enhanceDenoise").checked = !!flags.enhance_denoise;
  if ($("enhanceColorBoost")) $("enhanceColorBoost").checked = !!flags.enhance_color_boost;
  if ($("enhanceUltra")) $("enhanceUltra").checked = !!flags.enhance_ultra;
  if ($("enhanceExtreme")) $("enhanceExtreme").checked = !!flags.enhance_extreme;
  if ($("enhanceFaceRestore")) $("enhanceFaceRestore").checked = !!flags.enhance_face_restore;
  if ($("enhanceTwoPass")) $("enhanceTwoPass").checked = !!flags.enhance_two_pass;
  if ($("enhanceQualityGate")) $("enhanceQualityGate").checked = !!flags.enhance_quality_gate;
  if ($("enhanceTemporal")) $("enhanceTemporal").checked = !!flags.enhance_temporal;
  if ($("enhanceDeblock")) $("enhanceDeblock").checked = !!flags.enhance_deblock;
  if ($("enhanceMultiCandidate")) $("enhanceMultiCandidate").checked = !!flags.enhance_multicandidate;
  if ($("enhance10bit")) $("enhance10bit").checked = !!flags.enhance_10bit;
  if ($("enhanceAntiFlicker")) $("enhanceAntiFlicker").checked = !!flags.enhance_anti_flicker;
  if ($("enhanceSceneCut")) $("enhanceSceneCut").checked = !!flags.enhance_scene_cut;
}

function updateEnhanceSummary() {
  const flags = readEnhancements();
  const count = Number(!!flags.enhance_sharpen) + Number(!!flags.enhance_denoise) + Number(!!flags.enhance_color_boost) + Number(!!flags.enhance_ultra) + Number(!!flags.enhance_extreme) + Number(!!flags.enhance_face_restore) + Number(!!flags.enhance_two_pass) + Number(!!flags.enhance_quality_gate) + Number(!!flags.enhance_temporal) + Number(!!flags.enhance_deblock) + Number(!!flags.enhance_multicandidate) + Number(!!flags.enhance_10bit) + Number(!!flags.enhance_anti_flicker) + Number(!!flags.enhance_scene_cut);
  const el = $("enhanceSummary");
  if (!el) return;
  el.textContent = count > 0 ? t("runtime.enhance_summary_on", { n: count }) : t("runtime.enhance_summary_off");
}

function openEnhanceModal() {
  const modal = $("enhanceModal");
  if (!modal) {
    $("jobStatus").textContent = "Enhancements panel is unavailable. Reload application.";
    return;
  }
  modal.style.display = "flex";
  modal.classList.remove("hidden");
}

function closeEnhanceModal() {
  const modal = $("enhanceModal");
  if (!modal) return;
  modal.classList.add("hidden");
  modal.style.display = "none";
}

window.__w2lOpenEnhancements = openEnhanceModal;
window.__w2lCloseEnhancements = closeEnhanceModal;

function installEnhanceModalFallback() {
  document.addEventListener("click", (e) => {
    const t = e && e.target;
    if (!t || !t.closest) return;
    const openBtn = t.closest("#openEnhanceModalBtn");
    if (openBtn) {
      e.preventDefault();
      openEnhanceModal();
      return;
    }
    const closeBtn = t.closest("#closeEnhanceModalBtn");
    if (closeBtn) {
      e.preventDefault();
      closeEnhanceModal();
    }
  });
}

function updatePresetInfo() {
  const preset = $("runtimePreset");
  const info = $("presetInfo");
  if (!preset || !info) return;
  info.textContent = t(presetDescKey(preset.value));
}

function applyRuntimePresetToForm() {
  const preset = $("runtimePreset");
  if (!preset) return;
  const cfg = RUNTIME_PRESETS[preset.value] || RUNTIME_PRESETS.balanced;
  $("useBox").value = cfg.use_box;
  $("faceDetBatch").value = String(cfg.face_det_batch);
  $("wav2lipBatch").value = String(cfg.wav2lip_batch);
  $("padsValue").value = cfg.pads;
  $("resizeFactor").value = String(cfg.resize_factor);
  $("noSmooth").value = cfg.nosmooth;
  if (preset.value === "max" || preset.value === "max_plus") {
    const ck = $("checkpointPath");
    if (ck) {
      const cur = String(ck.value || "");
      if (/wav2lip\.pth/i.test(cur)) ck.value = cur.replace(/wav2lip\.pth/ig, "wav2lip_gan.pth");
      if (!cur.trim()) ck.value = "Wav2Lip\\checkpoints\\wav2lip_gan.pth";
    }
  }
  applyEnhancementsFlags(cfg);
  updatePresetInfo();
  updateEnhanceSummary();
}

async function applyCurrentRuntimeSettings() {
  await saveSettings();
}

function setProbeFrame(frameSrc) {
  const frame = $("probeFrame");
  const placeholder = $("probePlaceholder");
  const src = String(frameSrc || "").trim();
  if (!src) {
    frame.src = "";
    frame.classList.add("is-empty");
    if (placeholder) placeholder.classList.add("visible");
    $("probeBoxes").innerHTML = "";
    $("probeFacesList").innerHTML = "";
    return;
  }
  if (placeholder) placeholder.classList.remove("visible");
  frame.classList.remove("is-empty");
  frame.src = src;
}

function boolToSelectValue(v) {
  return v ? "1" : "0";
}

function selectToBool(v) {
  return String(v || "0") === "1";
}

function saveLastVideoId(videoId) {
  try {
    if (videoId) localStorage.setItem(LAST_VIDEO_ID_KEY, String(videoId));
    else localStorage.removeItem(LAST_VIDEO_ID_KEY);
  } catch (_) {}
}

function loadLastVideoId() {
  try {
    return String(localStorage.getItem(LAST_VIDEO_ID_KEY) || "").trim();
  } catch (_) {
    return "";
  }
}

function fmtFace(face) {
  if (!face) return t("face.not_selected");
  const b = face.bbox || {};
  return t("face.selected_fmt", { id: face.face_id, x: b.x, y: b.y, w: b.w, h: b.h });
}

function renderTimeline() {
  const list = $("timelineList");
  list.innerHTML = "";
  if (state.timelineSegments.length === 0) {
    list.textContent = t("timeline.empty");
    return;
  }
  state.timelineSegments.forEach((seg, idx) => {
    const row = document.createElement("div");
    row.className = "timeline-item";
    row.textContent = `#${idx + 1} ${seg.start_sec}s - ${seg.end_sec}s -> ${seg.speaker_face_id || "-"}`;

    const del = document.createElement("button");
    del.type = "button";
    del.textContent = t("timeline.delete");
    del.addEventListener("click", () => {
      state.timelineSegments.splice(idx, 1);
      renderTimeline();
    });

    row.appendChild(del);
    list.appendChild(row);
  });
}

function fmtTracking(track) {
  if (!track || !track.points || track.points.length === 0) return t("track.not_built");
  const cov = Number(track.coverage || 0) * 100;
  return t("track.ready_fmt", { points: track.points.length, coverage: cov.toFixed(1), step: track.sample_step });
}

function faceColorByIndex(index) {
  const palette = ["#ff4d4d", "#00b3ff", "#39d353", "#ffb020", "#b084ff", "#1dd3b0", "#ff6f91", "#ffd166"];
  return palette[index % palette.length];
}

// chunk-continue
function renderProbeFaces() {
  const boxes = $("probeBoxes");
  boxes.innerHTML = "";
  const faceList = $("probeFacesList");
  if (faceList) faceList.innerHTML = "";
  if (!state.probe || !state.probe.faces) return;

  const frameW = state.probe.frame_size.width || 1;
  const frameH = state.probe.frame_size.height || 1;
  const frameEl = $("probeFrame");
  const renderedW = Math.max(1, frameEl.clientWidth || frameW);
  const renderedH = Math.max(1, frameEl.clientHeight || Math.round((renderedW * frameH) / frameW));
  boxes.style.width = `${renderedW}px`;
  boxes.style.height = `${renderedH}px`;
  boxes.style.left = "0px";
  boxes.style.top = "0px";

  state.probe.faces.forEach((face, idx) => {
    const b = face.bbox;
    const color = faceColorByIndex(idx);
    const isActive = !!(state.selectedFace && state.selectedFace.face_id === face.face_id);

    const el = document.createElement("button");
    el.type = "button";
    el.className = `face-box${isActive ? " active" : ""}`;
    const x = Math.round((Number(b.x || 0) * renderedW) / frameW);
    const y = Math.round((Number(b.y || 0) * renderedH) / frameH);
    const w = Math.round((Number(b.w || 0) * renderedW) / frameW);
    const h = Math.round((Number(b.h || 0) * renderedH) / frameH);
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;
    el.style.width = `${Math.max(1, w)}px`;
    el.style.height = `${Math.max(1, h)}px`;
    el.style.borderColor = color;
    el.style.backgroundColor = `${color}33`;
    el.title = face.face_id;

    const badge = document.createElement("span");
    badge.className = "face-badge";
    badge.style.backgroundColor = color;
    badge.textContent = face.face_id;
    el.appendChild(badge);

    el.addEventListener("click", () => selectFace(face));
    boxes.appendChild(el);

    if (faceList) {
      const item = document.createElement("button");
      item.type = "button";
      item.className = `face-item${isActive ? " active" : ""}`;
      item.style.borderColor = color;
      item.textContent = `${face.face_id} (x:${b.x}, y:${b.y}, w:${b.w}, h:${b.h})`;
      item.addEventListener("click", () => selectFace(face));
      faceList.appendChild(item);
    }
  });
}

function jobItem(job) {
  const wrap = document.createElement("article");
  wrap.className = "job-item";
  const s = String(job.status || "").toLowerCase();

  const title = document.createElement("div");
  title.className = "job-title";
  title.textContent = `${job.id} - ${String(job.status || "").toUpperCase()}`;

  const meta = document.createElement("div");
  meta.className = "job-meta";
  meta.textContent = t("jobs.created_meta", { created: fmtTime(job.created_at), video: job.video_ref_id || "-" });

  const msg = document.createElement("div");
  msg.className = "job-meta job-message";
  msg.textContent = job.message || "";

  const progressValue = estimateJobProgress(job);
  const progressWrap = document.createElement("div");
  progressWrap.className = "job-progress";
  const progressTrack = document.createElement("div");
  progressTrack.className = "job-progress-track";
  const progressFill = document.createElement("div");
  progressFill.className = `job-progress-fill${s === "done" ? " is-done" : ""}${s === "failed" ? " is-failed" : ""}${s === "canceled" ? " is-canceled" : ""}`;
  progressFill.style.width = `${progressValue}%`;
  progressTrack.appendChild(progressFill);
  const progressText = document.createElement("div");
  progressText.className = "job-progress-text";
  progressText.textContent = `${t("jobs.progress")}: ${progressValue}%`;
  progressWrap.append(progressTrack, progressText);

  wrap.append(title, meta, msg, progressWrap);

  const actions = document.createElement("div");
  actions.className = "job-actions";

  if (job.target_face && job.target_face.face_id) {
    const target = document.createElement("div");
    target.className = "job-meta";
    target.textContent = t("jobs.target_face", { faceId: job.target_face.face_id });
    wrap.appendChild(target);
  }

  if (job.output_url) {
    const openBtn = document.createElement("button");
    openBtn.type = "button";
    openBtn.className = "job-open";
    openBtn.textContent = t("jobs.open_player");
    openBtn.addEventListener("click", async () => {
      try {
        await api("/api/output/open", { method: "POST", body: JSON.stringify({ job_id: job.id }) });
      } catch (err) {
        $("jobStatus").textContent = t("jobs.open_failed", { error: err.message });
      }
    });
    actions.appendChild(openBtn);

    const downloadBtn = document.createElement("button");
    downloadBtn.type = "button";
    downloadBtn.className = "job-download";
    downloadBtn.textContent = t("jobs.download");
    downloadBtn.addEventListener("click", () => {
      const a = document.createElement("a");
      a.href = job.output_url;
      a.rel = "noopener noreferrer";
      a.setAttribute("download", "");
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
      a.remove();
    });
    actions.appendChild(downloadBtn);
  }

  if (s === "failed" || s === "leased") {
    const rq = document.createElement("button");
    rq.type = "button";
    rq.textContent = t("jobs.requeue");
    rq.className = "job-requeue";
    rq.addEventListener("click", async () => {
      try {
        await api("/api/job/requeue", { method: "POST", body: JSON.stringify({ job_id: job.id }) });
        await refreshJobs();
      } catch (err) {
        $("jobStatus").textContent = t("jobs.requeue_error", { error: err.message });
      }
    });
    actions.appendChild(rq);
  }
  if (s === "queued" || s === "leased") {
    const cancelBtn = document.createElement("button");
    cancelBtn.type = "button";
    cancelBtn.textContent = t("jobs.cancel");
    cancelBtn.className = "job-cancel";
    cancelBtn.addEventListener("click", async () => {
      try {
        await api("/api/job/cancel", { method: "POST", body: JSON.stringify({ job_id: job.id }) });
        await refreshJobs();
      } catch (err) {
        $("jobStatus").textContent = t("jobs.cancel_failed", { error: err.message });
      }
    });
    actions.appendChild(cancelBtn);
  }
  if (s === "queued" || s === "done" || s === "failed" || s === "canceled") {
    const delBtn = document.createElement("button");
    delBtn.type = "button";
    delBtn.textContent = t("jobs.delete");
    delBtn.className = "job-delete";
    delBtn.addEventListener("click", async () => {
      try {
        await api("/api/job/delete", { method: "POST", body: JSON.stringify({ job_id: job.id }) });
        await refreshJobs();
      } catch (err) {
        $("jobStatus").textContent = t("jobs.delete_failed", { error: err.message });
      }
    });
    actions.appendChild(delBtn);
  }
  if (actions.childNodes.length) wrap.appendChild(actions);
  return wrap;
}

async function refreshJobs(options) {
  options = options || {};
  const list = $("jobsList");
  const showLoading = options.showLoading === true;
  const preserveScroll = options.preserveScroll !== false;
  const scrollHost = list && list.parentNode;
  const prevHostScrollTop = preserveScroll && scrollHost ? Number(scrollHost.scrollTop || 0) : null;
  if (showLoading) list.textContent = t("jobs.loading");
  try {
    const data = await api("/api/jobs", { method: "GET", headers: {} });
    const queueSizeEl = $("queueSize");
    if (queueSizeEl) queueSizeEl.textContent = t("jobs.queue", { n: data.queue_size || 0 });
    const st = data.stats || {};
    const jobsStatsEl = $("jobsStats");
    if (jobsStatsEl) jobsStatsEl.textContent = `q:${st.queued || 0} l:${st.leased || 0} r:${st.running || 0} d:${st.done || 0} f:${st.failed || 0} c:${st.canceled || 0}`;
    const fp = jobsFingerprint(data.jobs || []);
    if (fp === state.jobsFingerprint && list.childNodes.length > 0) {
      if (prevHostScrollTop !== null && scrollHost) scrollHost.scrollTop = prevHostScrollTop;
      return;
    }
    state.jobsFingerprint = fp;
    list.innerHTML = "";
    if (!data.jobs || data.jobs.length === 0) {
      list.textContent = t("jobs.empty");
      if (prevHostScrollTop !== null && scrollHost) scrollHost.scrollTop = prevHostScrollTop;
      return;
    }
    for (const job of data.jobs) list.appendChild(jobItem(job));
    if (prevHostScrollTop !== null && scrollHost) scrollHost.scrollTop = prevHostScrollTop;
  } catch (err) {
    list.textContent = t("jobs.load_error", { error: err.message });
  }
}

async function refreshConfig() {
  try {
    const data = await api("/api/config", { method: "GET", headers: {} });
    const modeText = data.mode === "command" ? t("pipeline.mode_command") : t("pipeline.mode_stub");
    const probe = data.probe_backend || "unknown";
    const execMode = data.exec_mode || "local";
    $("pipelineMode").textContent = t("pipeline.mode", { mode: modeText, exec: execMode, detector: probe });
    state.detectorMode = probe;
  } catch (err) {
    $("pipelineMode").textContent = t("config.error", { error: err.message });
  }
}

async function refreshSettings() {
  try {
    const data = await api("/api/settings", { method: "GET", headers: {} });
    const s = data.settings || {};
    $("execMode").value = s.exec_mode || "local";
    $("timeoutSec").value = s.timeout_sec || 3600;
    $("inferCommand").value = s.infer_command || "";
    $("checkpointPath").value = s.checkpoint_path || "";
    $("useBox").value = boolToSelectValue(!!s.use_box);
    $("faceDetBatch").value = Number(s.face_det_batch || 16);
    $("wav2lipBatch").value = Number(s.wav2lip_batch || 64);
    $("padsValue").value = s.pads || "0 10 0 0";
    $("resizeFactor").value = Number(s.resize_factor || 1);
    $("noSmooth").value = boolToSelectValue(!!s.nosmooth);
    applyEnhancementsFlags({
      enhance_sharpen: !!s.enhance_sharpen,
      enhance_denoise: !!s.enhance_denoise,
      enhance_color_boost: !!s.enhance_color_boost,
      enhance_ultra: !!s.enhance_ultra,
      enhance_extreme: !!s.enhance_extreme,
      enhance_face_restore: !!s.enhance_face_restore,
      enhance_two_pass: !!s.enhance_two_pass,
      enhance_quality_gate: !!s.enhance_quality_gate,
      enhance_temporal: !!s.enhance_temporal,
      enhance_deblock: !!s.enhance_deblock,
      enhance_multicandidate: !!s.enhance_multicandidate,
      enhance_10bit: !!s.enhance_10bit,
      enhance_anti_flicker: !!s.enhance_anti_flicker,
      enhance_scene_cut: !!s.enhance_scene_cut,
    });
    updateEnhanceSummary();
    $("settingsInfo").textContent = t("runtime.loaded");
  } catch (err) {
    $("settingsInfo").textContent = t("settings.load_error", { error: err.message });
  }
}

async function saveSettings() {
  const payload = {
    exec_mode: $("execMode").value,
    timeout_sec: Number($("timeoutSec").value || 3600),
    infer_command: $("inferCommand").value || "",
    checkpoint_path: $("checkpointPath").value || "",
    use_box: selectToBool($("useBox").value),
    face_det_batch: Number($("faceDetBatch").value || 16),
    wav2lip_batch: Number($("wav2lipBatch").value || 64),
    pads: $("padsValue").value || "0 10 0 0",
    resize_factor: Number($("resizeFactor").value || 1),
    nosmooth: selectToBool($("noSmooth").value),
    ...readEnhancements(),
  };
  try {
    const data = await api("/api/settings", { method: "POST", body: JSON.stringify(payload) });
    const s = (data && data.settings) || {};
    $("settingsInfo").textContent = t("runtime.saved", {
      box: s.use_box ? "on" : "off",
      detBatch: s.face_det_batch || "-",
      w2lBatch: s.wav2lip_batch || "-",
      pads: s.pads || "-",
    });
    applyEnhancementsFlags({
      enhance_sharpen: !!s.enhance_sharpen,
      enhance_denoise: !!s.enhance_denoise,
      enhance_color_boost: !!s.enhance_color_boost,
      enhance_ultra: !!s.enhance_ultra,
      enhance_extreme: !!s.enhance_extreme,
      enhance_face_restore: !!s.enhance_face_restore,
      enhance_two_pass: !!s.enhance_two_pass,
      enhance_quality_gate: !!s.enhance_quality_gate,
      enhance_temporal: !!s.enhance_temporal,
      enhance_deblock: !!s.enhance_deblock,
      enhance_multicandidate: !!s.enhance_multicandidate,
      enhance_10bit: !!s.enhance_10bit,
      enhance_anti_flicker: !!s.enhance_anti_flicker,
      enhance_scene_cut: !!s.enhance_scene_cut,
    });
    updateEnhanceSummary();
    await refreshConfig();
  } catch (err) {
    $("settingsInfo").textContent = t("settings.save_error", { error: err.message });
  }
}

async function autoProbeAtFirstSecond() {
  if (!state.videoId) return;
  const duration = Number(state.videoMeta && state.videoMeta.duration_sec);
  let ratio = 0.0;
  if (Number.isFinite(duration) && duration > 0) {
    ratio = Math.max(0, Math.min(1, 0.01 / duration));
  }
  $("probeRatio").value = String(Math.round(ratio * 100));
  const data = await api("/api/video/probe", { method: "POST", body: JSON.stringify({ video_id: state.videoId, frame_ratio: ratio }) });
  state.probe = data.probe;
  state.detectorMode = data.probe.detector_mode || state.detectorMode;
  const frameEl = $("probeFrame");
  frameEl.onload = () => renderProbeFaces();
  setProbeFrame(`data:image/jpeg;base64,${data.probe.frame_jpeg_b64}`);
  renderProbeFaces();
  $("selectedFaceInfo").textContent = data.probe.faces.length ? t("probe.preview_loaded_click") : t("probe.preview_loaded_none");
}

async function uploadVideo() {
  const input = $("videoUploadInput");
  const file = input.files && input.files[0];
  if (!file) {
    $("videoInfo").textContent = t("video.select_file");
    return;
  }
  const formData = new FormData();
  formData.append("video", file);
  $("videoInfo").textContent = t("video.uploading");
  try {
    const response = await fetch("/api/video/upload", { method: "POST", body: formData });
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || `HTTP ${response.status}`);
    state.videoId = data.video.id;
    saveLastVideoId(state.videoId);
    state.selectedFace = null;
    state.tracking = null;
    state.probe = null;
    state.timelineSegments = [];
    state.videoMeta = data.video.meta || null;
    renderTimeline();
    $("selectedFaceInfo").textContent = t("face.not_selected");
    $("trackingInfo").textContent = t("track.not_built");
    setTimelineEndFromVideoMeta();
    try {
      await autoProbeAtFirstSecond();
    } catch (err) {
      $("selectedFaceInfo").textContent = t("probe.error", { error: err.message });
    }
    $("videoInfo").textContent = t("video.uploaded", { videoId: state.videoId, meta: fmtVideoMeta(state.videoMeta) });
  } catch (err) {
    $("videoInfo").textContent = t("video.upload_error", { error: err.message });
  }
}

function resetSession() {
  saveLastVideoId("");
  state.videoId = "";
  state.videoMeta = null;
  state.probe = null;
  state.selectedFace = null;
  state.tracking = null;
  state.timelineSegments = [];
  $("videoUploadInput").value = "";
  $("audioInput").value = "";
  setProbeFrame("");
  $("segSpeaker").value = "";
  $("segStart").value = "0";
  $("segEnd").value = "3";
  renderTimeline();
  $("selectedFaceInfo").textContent = t("session.reset_selected");
  $("trackingInfo").textContent = t("track.not_built");
  $("videoInfo").textContent = t("session.reset_done");
  $("jobStatus").textContent = "";
}

function confirmAndResetSession() {
  const ok = window.confirm(t("session.reset_confirm"));
  if (!ok) return;
  resetSession();
}

async function restoreProbePreview() {
  if (!state.videoId) return;
  const ratio = Math.max(0, Math.min(1, Number(state.selectedFace && state.selectedFace.frame_ratio) || 0.5));
  $("probeRatio").value = String(Math.round(ratio * 100));
  const data = await api("/api/video/probe", { method: "POST", body: JSON.stringify({ video_id: state.videoId, frame_ratio: ratio }) });
  state.probe = data.probe;
  state.detectorMode = (data.probe && data.probe.detector_mode) || state.detectorMode;
  const frameEl = $("probeFrame");
  frameEl.onload = () => renderProbeFaces();
  setProbeFrame(`data:image/jpeg;base64,${data.probe.frame_jpeg_b64}`);
  renderProbeFaces();
}

async function restorePipelineContext() {
  const savedVideoId = loadLastVideoId();
  if (!savedVideoId) return;
  try {
    const encoded = encodeURIComponent(savedVideoId);
    const [metaResp, selectionResp, trackingResp, timelineResp] = await Promise.all([
      api(`/api/video/meta?video_id=${encoded}`, { method: "GET", headers: {} }),
      api(`/api/face/selection?video_id=${encoded}`, { method: "GET", headers: {} }),
      api(`/api/tracking?video_id=${encoded}`, { method: "GET", headers: {} }),
      api(`/api/timeline?video_id=${encoded}`, { method: "GET", headers: {} }),
    ]);
    state.videoId = savedVideoId;
    state.videoMeta = metaResp.meta || null;
    state.selectedFace = (selectionResp && selectionResp.selection) || null;
    state.tracking = (trackingResp && trackingResp.track) || null;
    state.timelineSegments = timelineResp && timelineResp.timeline && Array.isArray(timelineResp.timeline.segments)
      ? timelineResp.timeline.segments
      : [];
    try {
      await restoreProbePreview();
    } catch (_) {}
    renderTimeline();
    if (!state.timelineSegments || state.timelineSegments.length === 0) setTimelineEndFromVideoMeta();
    $("selectedFaceInfo").textContent = fmtFace(state.selectedFace);
    $("trackingInfo").textContent = fmtTracking(state.tracking);
    if (state.selectedFace && state.selectedFace.face_id) $("segSpeaker").value = state.selectedFace.face_id;
    $("videoInfo").textContent = t("video.restored", { videoId: state.videoId, meta: fmtVideoMeta(state.videoMeta) });
  } catch (err) {
    saveLastVideoId("");
    $("videoInfo").textContent = t("video.restore_unavailable", { error: err.message });
  }
}
async function probeVideo() {
  if (!state.videoId) {
    $("selectedFaceInfo").textContent = t("video.upload_first");
    return;
  }
  const frameRatio = Number($("probeRatio").value || 50) / 100.0;
  $("selectedFaceInfo").textContent = t("face.detecting");
  try {
    const data = await api("/api/video/probe", { method: "POST", body: JSON.stringify({ video_id: state.videoId, frame_ratio: frameRatio }) });
    state.probe = data.probe;
    state.detectorMode = data.probe.detector_mode || state.detectorMode;
    const frameEl = $("probeFrame");
    frameEl.onload = () => renderProbeFaces();
    setProbeFrame(`data:image/jpeg;base64,${data.probe.frame_jpeg_b64}`);
    renderProbeFaces();
    $("selectedFaceInfo").textContent = data.probe.faces.length ? t("face.click_select") : t("face.none_found_retry");
  } catch (err) {
    $("selectedFaceInfo").textContent = t("probe.error", { error: err.message });
  }
}

async function selectFace(face) {
  if (!state.videoId || !state.probe) return;
  try {
    const data = await api("/api/face/select", {
      method: "POST",
      body: JSON.stringify({
        video_id: state.videoId,
        face_id: face.face_id,
        bbox: face.bbox,
        frame_ratio: state.probe.frame_ratio,
        detector_mode: state.detectorMode,
      }),
    });
    state.selectedFace = data.selection;
    state.tracking = null;
    renderProbeFaces();
    $("selectedFaceInfo").textContent = fmtFace(state.selectedFace);
    $("trackingInfo").textContent = t("face.updated_rebuild");
    $("segSpeaker").value = state.selectedFace.face_id;
  } catch (err) {
    $("selectedFaceInfo").textContent = t("face.selection_error", { error: err.message });
  }
}

async function buildTracking() {
  if (!state.videoId) return void ($("trackingInfo").textContent = t("video.upload_first"));
  if (!state.selectedFace) return void ($("trackingInfo").textContent = t("face.select_first"));
  const sampleStep = Number($("trackStep").value || 3);
  $("trackingInfo").textContent = t("track.building");
  try {
    const data = await api("/api/tracking/build", { method: "POST", body: JSON.stringify({ video_id: state.videoId, sample_step: sampleStep }) });
    state.tracking = data.track;
    $("trackingInfo").textContent = fmtTracking(state.tracking);
  } catch (err) {
    $("trackingInfo").textContent = t("track.error", { error: err.message });
  }
}

function addTimelineSegment() {
  let start = Number($("segStart").value);
  let end = Number($("segEnd").value);
  const speaker = String($("segSpeaker").value || "").trim();
  const maxDuration = Number(state.videoMeta && state.videoMeta.duration_sec);
  if (Number.isFinite(maxDuration) && maxDuration > 0) {
    start = Math.max(0, Math.min(start, maxDuration));
    end = Math.max(0, Math.min(end, maxDuration));
    $("segStart").value = String(start);
    $("segEnd").value = String(end);
  }
  if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) {
    $("jobStatus").textContent = t("timeline.invalid_segment");
    return;
  }
  state.timelineSegments.push({ start_sec: start, end_sec: end, speaker_face_id: speaker });
  renderTimeline();
}

async function saveTimeline() {
  if (!state.videoId) return void ($("jobStatus").textContent = t("video.upload_first"));
  try {
    const data = await api("/api/timeline/save", { method: "POST", body: JSON.stringify({ video_id: state.videoId, segments: state.timelineSegments }) });
    state.timelineSegments = (data.timeline && data.timeline.segments) || [];
    renderTimeline();
    const stats = (data.timeline && data.timeline.stats) || {};
    $("jobStatus").textContent = t("timeline.saved", {
      saved: stats.saved_count || state.timelineSegments.length,
      input: stats.input_count || state.timelineSegments.length,
      dropped: stats.dropped_invalid || 0,
      overlap: stats.adjusted_overlap || 0,
      merged: stats.merged_same_speaker || 0,
      max: fmtSeconds(stats.duration_sec),
    });
  } catch (err) {
    $("jobStatus").textContent = t("timeline.save_error", { error: err.message });
  }
}

async function submitJob() {
  const status = $("jobStatus");
  const audioFile = $("audioInput").files && $("audioInput").files[0];
  if (!state.videoId) return void (status.textContent = t("video.upload_first"));
  if (!state.selectedFace) return void (status.textContent = t("face.select_first"));
  if (!audioFile) return void (status.textContent = t("audio.select_file"));
  if (!state.tracking || !state.tracking.points || state.tracking.points.length === 0) {
    status.textContent = t("job.submit_build_tracking");
    return;
  }
  const formData = new FormData();
  formData.append("video_id", state.videoId);
  formData.append("audio", audioFile);
  status.textContent = t("job.submitting");
  $("submitBtn").disabled = true;
  try {
    const response = await fetch("/api/job/submit", { method: "POST", body: formData });
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || `HTTP ${response.status}`);
    status.textContent = t("job.created", { jobId: data.job.id });
    $("audioInput").value = "";
    await refreshJobs();
  } catch (err) {
    status.textContent = t("job.submit_error", { error: err.message });
  } finally {
    $("submitBtn").disabled = false;
  }
}

async function onWindowDragStart(evt) {
  if (evt.target.closest(".window-actions")) return;
  if (evt.target.closest("button") || evt.target.closest("select")) return;
  try {
    const rect = await api("/api/window/rect", { method: "GET", headers: {} });
    if (!rect.ok) return;
    state.dragging = true;
    state.dragOffsetX = evt.screenX - rect.left;
    state.dragOffsetY = evt.screenY - rect.top;
  } catch (_) {}
}

async function onWindowDragMove(evt) {
  if (!state.dragging) return;
  const left = evt.screenX - state.dragOffsetX;
  const top = evt.screenY - state.dragOffsetY;
  try {
    await api("/api/window/move", { method: "POST", body: JSON.stringify({ left, top }) });
  } catch (_) {}
}

function onWindowDragEnd() {
  state.dragging = false;
}

function onProbeRatioInput() {
  if (!state.videoId) return;
  if (state.probeDebounce) window.clearTimeout(state.probeDebounce);
  state.probeDebounce = window.setTimeout(() => {
    state.probeDebounce = 0;
    probeVideo();
  }, 180);
}

function init() {
  state.lang = loadLang();
  applyStaticI18n();
  const langSelect = $("langSelect");
  if (langSelect) {
    langSelect.value = state.lang;
    langSelect.addEventListener("change", (e) => setLanguage(e.target.value));
    langSelect.addEventListener("input", (e) => setLanguage(e.target.value));
  }

  $("uploadVideoBtn").addEventListener("click", uploadVideo);
  $("videoUploadInput").addEventListener("change", () => {
    const input = $("videoUploadInput");
    if (input && input.files && input.files[0]) uploadVideo();
  });
  $("resetSessionBtn").addEventListener("click", confirmAndResetSession);
  $("applyPresetBtn").addEventListener("click", async () => {
    await applyCurrentRuntimeSettings();
  });
  $("runtimePreset").addEventListener("change", () => {
    applyRuntimePresetToForm();
  });
  const openEnhBtn = $("openEnhanceModalBtn");
  const closeEnhBtn = $("closeEnhanceModalBtn");
  const enhanceModal = $("enhanceModal");
  if (openEnhBtn) openEnhBtn.addEventListener("click", openEnhanceModal);
  if (closeEnhBtn) closeEnhBtn.addEventListener("click", closeEnhanceModal);
  if (enhanceModal) {
    enhanceModal.addEventListener("click", (e) => {
      if (e.target === enhanceModal) closeEnhanceModal();
    });
  }
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeEnhanceModal();
  });
  const saveEnhBtn = $("saveEnhanceBtn");
  if (saveEnhBtn) {
    saveEnhBtn.addEventListener("click", async () => {
      updateEnhanceSummary();
      closeEnhanceModal();
      await saveSettings();
    });
  }
  const enhSharpen = $("enhanceSharpen");
  const enhDenoise = $("enhanceDenoise");
  const enhColor = $("enhanceColorBoost");
  const enhUltra = $("enhanceUltra");
  const enhExtreme = $("enhanceExtreme");
  const enhFaceRestore = $("enhanceFaceRestore");
  const enhTwoPass = $("enhanceTwoPass");
  const enhQualityGate = $("enhanceQualityGate");
  const enhTemporal = $("enhanceTemporal");
  const enhDeblock = $("enhanceDeblock");
  const enhMultiCandidate = $("enhanceMultiCandidate");
  const enh10bit = $("enhance10bit");
  const enhAntiFlicker = $("enhanceAntiFlicker");
  const enhSceneCut = $("enhanceSceneCut");
  if (enhSharpen) enhSharpen.addEventListener("change", updateEnhanceSummary);
  if (enhDenoise) enhDenoise.addEventListener("change", updateEnhanceSummary);
  if (enhColor) enhColor.addEventListener("change", updateEnhanceSummary);
  if (enhUltra) enhUltra.addEventListener("change", updateEnhanceSummary);
  if (enhExtreme) enhExtreme.addEventListener("change", updateEnhanceSummary);
  if (enhFaceRestore) enhFaceRestore.addEventListener("change", updateEnhanceSummary);
  if (enhTwoPass) enhTwoPass.addEventListener("change", updateEnhanceSummary);
  if (enhQualityGate) enhQualityGate.addEventListener("change", updateEnhanceSummary);
  if (enhTemporal) enhTemporal.addEventListener("change", updateEnhanceSummary);
  if (enhDeblock) enhDeblock.addEventListener("change", updateEnhanceSummary);
  if (enhMultiCandidate) enhMultiCandidate.addEventListener("change", updateEnhanceSummary);
  if (enh10bit) enh10bit.addEventListener("change", updateEnhanceSummary);
  if (enhAntiFlicker) enhAntiFlicker.addEventListener("change", updateEnhanceSummary);
  if (enhSceneCut) enhSceneCut.addEventListener("change", updateEnhanceSummary);
  $("probeBtn").addEventListener("click", probeVideo);
  $("probeRatio").addEventListener("input", onProbeRatioInput);
  $("probeRatio").addEventListener("change", onProbeRatioInput);
  $("buildTrackBtn").addEventListener("click", buildTracking);
  $("addSegBtn").addEventListener("click", addTimelineSegment);
  $("saveTimelineBtn").addEventListener("click", saveTimeline);
  $("submitBtn").addEventListener("click", submitJob);
  $("refreshBtn").addEventListener("click", () => refreshJobs({ showLoading: true, preserveScroll: true }));

  $("minBtn").addEventListener("click", () => windowAction("minimize"));
  $("maxBtn").addEventListener("click", () => windowAction("maximize"));
  $("closeBtn").addEventListener("click", () => windowAction("close"));

  const drag = $("windowDragBar");
  drag.addEventListener("mousedown", onWindowDragStart);
  window.addEventListener("mousemove", onWindowDragMove);
  window.addEventListener("mouseup", onWindowDragEnd);
  window.addEventListener("resize", () => {
    if (state.probe && state.probe.faces && state.probe.faces.length) renderProbeFaces();
  });

  renderTimeline();
  setProbeFrame("");
  updatePresetInfo();
  updateEnhanceSummary();
  installEnhanceModalFallback();
  refreshSettings();
  refreshConfig();
  restorePipelineContext();
  refreshJobs({ showLoading: true, preserveScroll: false });
  state.pollTimer = window.setInterval(() => refreshJobs({ showLoading: false, preserveScroll: true }), 2000);
}

init();
