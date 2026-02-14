# Development Progress
## 2026-02-14 (GitHub README redesign + screenshots + license)
- README полностью переработан под GitHub-подачу (`README.md`):
  - обновлен бренд на `LipFlow`,
  - добавлена крупная кнопка `Download Portable (Google Drive)` с placeholder-ссылкой,
  - добавлены скриншоты `1.png` и `2.png` в секцию `Screenshots`,
  - структура упрощена: Quick Start, Portable Distribution, Runtime Notes, API, License, Disclaimer.
- Добавлен файл `LICENSE` с mixed licensing моделью:
  - MIT для собственного wrapper-кода проекта,
  - явные исключения для third-party компонентов (`Wav2Lip/`, модели, внешние бинарники),
  - зафиксировано, что для Wav2Lip действуют исходные upstream-ограничения (включая non-commercial условия).

## 2026-02-14 (Title bar rename to LipFlow + post-flatten path validation)
- В программе изменено название только в title bar на `LipFlow`:
  - `app/web/index.html` (`<title>` и `<strong>` в custom window bar),
  - `app/launcher.py` (`window_title` и fallback MessageBox caption).
- После переноса структуры в корень выполнена проверка путей:
  - `portable_check.bat` -> `PASS`,
  - `node --check app/web/app.js` успешно,
  - `app/python/python.exe -m compileall app/main.py app/launcher.py app/workers/wav2lip_runner.py` успешно,
  - launch-скрипты (`only_*.bat`, `debug_*.bat`) используют валидные относительные пути от корня.

## 2026-02-14 (GitHub layout flattening for repo name LipFlow)
- Для публикации на GitHub подготовлена плоская структура репозитория:
  - содержимое `Wav2LipViewer/` поднято в корень workspace,
  - пустая папка `Wav2LipViewer` удалена.
- Внутренние имена/брендинг приложения не менялись (по требованию: название меняется только на стороне GitHub-репозитория).
- Корневой `.gitignore` синхронизирован с новой структурой (пути без префикса `Wav2LipViewer/`).
- README (`GitHub deployment`) обновлен под текущие пути (`Wav2Lip/.git` вместо `Wav2LipViewer/Wav2Lip/.git`).

## 2026-02-14 (GitHub source-only deploy profile prepared)
- Подготовлен профиль публикации на GitHub без тяжелых portable-артефактов:
  - добавлен корневой `.gitignore` с исключениями для:
    - `Wav2LipViewer/app/python` (embedded Python),
    - `Wav2LipViewer/app/bin/ffmpeg`,
    - `Wav2LipViewer/Wav2Lip/checkpoints`,
    - runtime-data/cache/logs (`app/data/videos|audios|outputs|temp|cef_cache|jobs`, `app/logs`),
    - локального wheel-кэша `Wav2LipViewer/wheels`.
- README обновлен разделом `GitHub deployment (source-only)`:
  - зафиксировано, что portable-версия распространяется отдельно архивом,
  - добавлен placeholder под ссылку Google Drive (`<PASTE_GOOGLE_DRIVE_LINK_HERE>`),
  - добавлено предупреждение про вложенный `.git` в `Wav2LipViewer/Wav2Lip` и команда удаления перед первым `git add`.

## 2026-02-14 (Unicode upload filenames + RU i18n completion pass)
- Исправлена загрузка файлов с кириллицей и другими Unicode-символами в имени:
  - в `Wav2LipViewer/app/main.py` удалено использование `secure_filename` (ASCII-only поведение),
  - добавлен `_safe_upload_filename(...)`:
    - сохраняет Unicode (включая кириллицу),
    - удаляет path-инъекции (`/`, `\`), запрещенные для Windows символы и управляющие символы,
    - нормализует имя и оставляет валидное расширение.
- `api/video/upload` и `api/job/submit` переведены на новый sanitizer:
  - теперь `.mp4/.wav/...` с кириллическими именами корректно проходят валидацию и сохраняются.
- Доработана локализация интерфейса (`Wav2LipViewer/app/web/app.js`):
  - вынесены в I18N и переведены runtime-сообщения (upload/probe/tracking/timeline/jobs/settings/config),
  - убраны оставшиеся hardcoded-строки из рабочих сценариев,
  - расширен RU-словарь по кнопкам/лейблам, где оставался английский текст.
- Исправлен дефолтный checkpoint fallback в пресете:
  - `Wav2Lip\checkpoints\wav2lip_gan.pth` (вместо старого `..\Wav2Lip\...`).
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно,
  - `Wav2LipViewer/app/python/python.exe -m compileall Wav2LipViewer/app/main.py` успешно.

## 2026-02-14 (Wav2Lip moved inside Wav2LipViewer + path migration)
- Выполнен перенос репозитория модели:
  - из `wav2lip/Wav2Lip`
  - в `wav2lip/Wav2LipViewer/Wav2Lip`.
- Актуализированы пути во всех запускных скриптах и проверках:
  - `only_gpu.bat`, `only_cpu.bat`, `debug_gpu.bat`, `debug_cpu.bat`
  - `portable_check.bat`
  - `set_wav2lip_env.example.bat`.
- Backend адаптирован под новый layout:
  - `Wav2LipViewer/app/main.py` (`_portable_checkpoint_candidates` теперь ищет внутри `Wav2LipViewer/Wav2Lip`).
- Runtime настройки обновлены под новый относительный checkpoint path:
  - `Wav2LipViewer/app/data/runtime_settings.json` -> `Wav2Lip\\checkpoints\\wav2lip_gan.pth`.
- README обновлен под новую структуру (`Wav2Lip\\...` вместо `..\\Wav2Lip\\...`).
- Верификация:
  - `python -m compileall` для `app/main.py` и `app/workers/wav2lip_runner.py` успешно,
  - `portable_check.bat` -> `PASS`.

## 2026-02-14 (Project cleanup: caches/artifacts/backups)
- Выполнена ручная очистка проекта от ненужных файлов без затрагивания рабочих бинарников и checkpoint-моделей.
- Удалены runtime-артефакты:
  - `Wav2LipViewer/app/data/videos/*`
  - `Wav2LipViewer/app/data/audios/*`
  - `Wav2LipViewer/app/data/outputs/*`
  - `Wav2LipViewer/app/data/temp/*`
  - `Wav2LipViewer/app/data/cef_cache/*`
  - `Wav2LipViewer/app/logs/*`
- Удалены Python-кэши во всем workspace (`Wav2LipViewer`, `Wav2Lip`):
  - все каталоги `__pycache__`
  - все файлы `*.pyc`/`*.pyo`
- Удалены backup-файлы checkpoint:
  - `Wav2Lip/checkpoints/*.bak`
- Верификация после очистки:
  - runtime-папки артефактов пустые,
  - `__pycache__`/`*.pyc`/`*.bak` отсутствуют,
  - критичные файлы на месте: `app/python/python.exe`, `app/bin/ffmpeg/ffmpeg.exe`, `wav2lip*.pth`.

## 2026-02-14 (Startup auto-clean of stale media artifacts)
- Добавлена автоматическая очистка на запуске приложения:
  - очищаются содержимое `app/data/videos`, `app/data/audios`, `app/data/outputs`, `app/data/temp`,
  - сбрасываются JSON-индексы и очередь задач: `jobs.json`, `video_index.json`, `face_selections.json`, `timelines.json`, `face_tracks.json`.
- `runtime_settings.json` не затрагивается (настройки пользователя сохраняются).
- Обновлены:
  - `Wav2LipViewer/app/main.py`
  - `Wav2LipViewer/README.md`.
- Верификация:
  - `Wav2LipViewer/app/python/python.exe -m compileall Wav2LipViewer/app/main.py` успешно.

## 2026-02-14 (Extended video format support + codec normalize fallback)
- Расширена поддержка контейнеров загрузки видео в `api/video/upload`:
  - добавлены: `.m4v`, `.ts`, `.mts`, `.m2ts`, `.flv`, `.wmv`, `.mpeg`, `.mpg`, `.3gp`, `.ogv` (в дополнение к `mp4/mov/avi/mkv/webm`).
- Добавлен fallback для «проблемных» файлов (включая часть `.mp4`, которые не читаются OpenCV из-за codec/profile):
  - если после upload видео не декодируется для метаданных/probe, сервер автоматически нормализует файл через bundled `ffmpeg` в `H.264 + yuv420p + AAC` (`*_normalized.mp4`),
  - после нормализации файл используется дальше прозрачно для UI/пайплайна.
- Метаданные видео усилены fallback-ом через `ffprobe` (`_read_video_meta_ffprobe`) на случай ограничений OpenCV backend.
- Обновлены:
  - `Wav2LipViewer/app/main.py`
  - `Wav2LipViewer/README.md`.
- Верификация:
  - `Wav2LipViewer/app/python/python.exe -m compileall Wav2LipViewer/app/main.py` успешно.

## 2026-02-14 (UI hotfix: visible global outline + Jobs download button)
- Исправлена рамка окна, которая в CEF отображалась как точка в углу:
  - убран pseudo-element c `inset`,
  - контур окна сделан через совместимый `outline` + `outline-offset` на `.app-shell`.
- В `Jobs` заменен `Download` с гиперссылки на обычную кнопку рядом с остальными action-кнопками.
  - загрузка выполняется программно через временный `<a download>` по клику.
- Обновлены:
  - `Wav2LipViewer/app/web/styles.css`
  - `Wav2LipViewer/app/web/app.js`
  - `Wav2LipViewer/app/web/index.html` (cache-busting `v=20260214_03`).
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.

## 2026-02-14 (Jobs wrap fix + global window outline)
- Исправлен UX проблемы горизонтального скролла в блоке `Jobs` при длинных `job.message` (большой список enhancement-флагов):
  - сообщения задач теперь принудительно переносятся по словам/символам (`overflow-wrap:anywhere`, `word-break:break-word`),
  - карточки задач растут по вертикали вместо растягивания по горизонтали,
  - для правой карточки jobs включен режим `overflow-y: auto` + `overflow-x: hidden`, чтобы горизонтальный скролл в jobs не появлялся.
- Добавлена аккуратная обводка по периметру всего окна приложения:
  - в `app-shell` добавлен overlay-контур через `::after` с тонкой рамкой и легкой внутренней подсветкой.
- Обновлены:
  - `Wav2LipViewer/app/web/styles.css`
  - `Wav2LipViewer/app/web/app.js`
  - `Wav2LipViewer/app/web/index.html` (cache-busting `v=20260214_02`).
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.

## 2026-02-14 (Portable hardening + transfer readiness audit)
- Проведен аудит переносимости `Wav2LipViewer` и устранены практические блокеры для переноса на другую Windows x64 без установки Python/pip.
- Исправлены критичные риски:
  - `app/data/runtime_settings.json`: убран machine-specific абсолютный `checkpoint_path`, заменен на переносимый относительный путь `..\\Wav2Lip\\checkpoints\\wav2lip_gan.pth`.
  - `Wav2LipViewer/app/main.py`: добавлена авто-нормализация `checkpoint_path` в runtime settings:
    - если сохраненный путь не существует после переноса, сервис автоматически переключается на валидный default/env/candidate checkpoint.
- Улучшены launch-скрипты:
  - `only_gpu.bat`, `only_cpu.bat`, `debug_gpu.bat`, `debug_cpu.bat`:
    - добавлен fallback-выбор checkpoint (если preferred отсутствует, берется альтернативный `wav2lip*.pth`).
- Добавлен self-check переносимости:
  - новый `Wav2LipViewer/portable_check.bat` проверяет наличие обязательных bundled файлов (embedded Python, launcher, web, ffmpeg/ffprobe) и ключевых Wav2Lip-ассетов.
- README обновлен:
  - добавлен раздел `Portability notes` с явными условиями переносимости,
  - добавлен шаг пред-переносной проверки `portable_check.bat`.
- Верификация:
  - `Wav2LipViewer/app/python/python.exe -m compileall Wav2LipViewer/app/main.py` успешно.
  - `portable_check.bat` добавлен как стандартный pre-transfer smoke-check.

## 2026-02-14 (Scene-cut aware anti-flicker guard)
- Продолжили roadmap пункт `Scene-cut aware обработка` через новый флаг `enhance_scene_cut`.
- Backend (`Wav2LipViewer/app/main.py`):
  - добавлен `W2L_ENHANCE_SCENE_CUT` (env/defaults/runtime env),
  - `POST /api/settings` и runtime settings расширены полем `enhance_scene_cut`,
  - в postprocess добавлен scene-cut probe:
    - анализ плотности склеек через `ffmpeg` (`select='gt(scene,0.30)',showinfo`),
    - при высокой плотности склеек anti-flicker (`tmix`) автоматически отключается, чтобы избежать ghosting на монтажных стыках,
    - в job message добавляется диагностический суффикс `scene_guard_on/off(...)`.
- UI (`Wav2LipViewer/app/web/index.html`, `Wav2LipViewer/app/web/app.js`):
  - новый чекбокс `Scene-cut aware guard` в `Enhancements`,
  - добавлены EN/RU i18n подписи/описания,
  - флаг подключен в form read/write, `GET/POST /api/settings`, summary counter и runtime presets (`Maximum`/`Maximum+` включают guard по умолчанию).
- Документация:
  - `Wav2LipViewer/README.md` дополнен `W2L_ENHANCE_SCENE_CUT` и новым полем в `POST /api/settings`.
- Cache-busting обновлен:
  - `styles.css?v=20260214_01`
  - `app.js?v=20260214_01`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно,
  - `Wav2LipViewer/app/python/python.exe -m compileall Wav2LipViewer/app/main.py` успешно.

## 2026-02-12 (Next proposals from assistant)
- Quality roadmap на следующий этап:
  1. Интеграция `GFPGAN/CodeFormer` для ROI лица после Wav2Lip.
  2. Интеграция `Real-ESRGAN` для face-crop с мягким blend обратно в кадр.
  3. Optical-flow стабилизация ROI лица между кадрами (снижение jitter).
  4. Seam-aware compositing (Poisson/Laplacian blend) вместо простого наложения.
  5. Адаптивная маска рта/подбородка по движению и уверенности детектора.
  6. Scene-cut aware обработка (отдельная логика на резких склейках).
  7. Multi-candidate + метрики выбора лучшего результата (LPIPS/SSIM/LSE proxy).
  8. 10-bit internal pipeline по всей цепочке до финального downcast.
  9. CUDA/libplacebo тяжёлые пост-фильтры для high-end GPU.
- Примечание: auto-profile по GPU/VRAM сознательно исключен по договоренности.
## 2026-02-12 (Preset UX logic fix)
- Изменена логика пресетов по UX:
  - выбор пресета в выпадающем списке сразу подставляет значения в форму (без автосохранения),
  - кнопка `Apply preset` теперь сохраняет текущие значения формы (включая ручные правки чекбоксов).
- Это устраняет конфликт, когда `Apply` перезатирал ручные изменения выбранным preset.
- Обновлены:
  - `Wav2LipViewer/app/web/app.js`
  - `Wav2LipViewer/app/web/index.html` (cache-busting `v=20260212_17`).
- Верификация: `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (UX fix: Apply preset now saves immediately)
- Убран отдельный `Save settings` из Runtime Settings (источник путаницы).
- Кнопка `Apply preset` теперь выполняет и применение, и сохранение за один клик (`apply + save`).
- Обновлены файлы:
  - `Wav2LipViewer/app/web/index.html`
  - `Wav2LipViewer/app/web/app.js`
- Cache-busting обновлен до `v=20260212_16`.
- Верификация: `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (Maximum quality pass v2: +4 heavy postprocess upgrades)
- Добавлены еще 4 улучшалки для максимального качества (без auto-profile):
  - `enhance_deblock`
  - `enhance_multicandidate`
  - `enhance_10bit`
  - `enhance_anti_flicker`
- UI (`Wav2LipViewer/app/web/index.html`, `Wav2LipViewer/app/web/app.js`):
  - новые чекбоксы в `Enhancements`,
  - EN/RU i18n подписи и описания,
  - пресеты обновлены: `Maximum` и `Maximum+` включают весь новый стек.
- Backend (`Wav2LipViewer/app/main.py`):
  - новые флаги проведены через runtime env / defaults / `POST /api/settings`,
  - postprocess расширен:
    - deblock-pass для артефактов компрессии,
    - anti-flicker blend-pass,
    - multi-candidate render с выбором лучшего результата,
    - 10-bit intermediate pipeline с финальным downcast в `yuv420p`.
- README обновлен:
  - добавлены новые env-переменные и поля `POST /api/settings`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно,
  - `python -m compileall Wav2LipViewer/app/main.py` успешно.
## 2026-02-12 (Maximum quality toolkit: 4 new enhancement toggles fully wired)
- Завершена полная интеграция 4 новых улучшалок в UI + backend:
  - `enhance_face_restore`
  - `enhance_two_pass`
  - `enhance_quality_gate`
  - `enhance_temporal`
- Backend (`Wav2LipViewer/app/main.py`) обновлен:
  - флаги добавлены в `runtime_env` для воркера,
  - добавлены в runtime defaults,
  - добавлены в `POST /api/settings` (чтение/сохранение).
- Постпроцесс теперь поддерживает:
  - `face_restore`: усиленное восстановление деталей (`cas` + дополнительный `unsharp`),
  - `two_pass`: второй проход refine-фильтров и более тяжелого encode,
  - `temporal`: temporal denoise для межкадровой стабильности,
  - `quality_gate`: проверку битрейта через `ffprobe` и авто-rerender при просадке качества.
- Добавлен resolver `ffprobe`:
  - сначала `app/bin/ffmpeg/ffprobe.exe`, fallback на `ffprobe` из `PATH`.
- Документация обновлена:
  - `Wav2LipViewer/README.md` дополнен новыми env-флагами и параметрами `/api/settings`.
- Верификация:
  - `python -m compileall Wav2LipViewer/app/main.py` успешно,
  - `node --check Wav2LipViewer/app/web/app.js` успешно.

## 2026-02-12 (Maximum+ final tuning: GAN preference + extreme quality stack)
- Для `Maximum`/`Maximum+` пресетов добавлен авто-переход на `wav2lip_gan.pth` (если в поле checkpoint был `wav2lip.pth` или поле было пустым).
- `Maximum+` закреплен как самый тяжелый профиль:
  - `face_det_batch=1`, `wav2lip_batch=4`,
  - включены `sharpen + denoise + color + ultra + extreme`.
- Добавлен новый чекбокс `Extreme encode pass (very slow)` (`enhance_extreme`) в UI + EN/RU i18n.
- Backend `enhance_extreme`:
  - дополнительные фильтры `nlmeans + gradfun`,
  - encode до `preset=placebo`, `crf=12`, `tune=film`.
- Runtime/API/README обновлены для `enhance_extreme` / `W2L_ENHANCE_EXTREME`.
- Обновлен cache-busting:
  - `styles.css?v=20260212_13`
  - `app.js?v=20260212_13`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно,
  - `python -m compileall Wav2LipViewer/app/main.py` успешно.
## 2026-02-12 (Maximum+ preset + Extreme quality pass)
- В UI добавлен новый пресет `Maximum+ quality`.
- В `Enhancements` добавлен новый флаг:
  - `Extreme encode pass (very slow)` (`enhance_extreme`).
- Пресеты обновлены:
  - `Maximum` = heavy quality,
  - `Maximum+` = максимально тяжелый режим (`face_det_batch=1`, `wav2lip_batch=4`, все улучшалки + extreme).
- Backend postprocess расширен полем `enhance_extreme`:
  - добавлены фильтры `nlmeans` + `gradfun`,
  - encode усилен до `preset=placebo`, `crf=12`, `tune=film`.
- Runtime/API/README расширены новым полем `enhance_extreme` и env `W2L_ENHANCE_EXTREME`.
- Обновлен cache-busting:
  - `styles.css?v=20260212_13`
  - `app.js?v=20260212_13`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно,
  - `python -m compileall Wav2LipViewer/app/main.py` успешно.
## 2026-02-12 (quality push: Ultra postprocess + stronger Maximum preset)
- В блок `Enhancements` добавлен новый флаг:
  - `Ultra postprocess (slow)` (`enhance_ultra`) для максимально тяжелого постпроцесса.
- В `Maximum` preset усилены параметры:
  - `face_det_batch=2`, `wav2lip_batch=8` (более тяжелый режим),
  - включены все улучшалки, включая `enhance_ultra`.
- Backend postprocess в `Wav2LipViewer/app/main.py` расширен для `enhance_ultra`:
  - добавлены фильтры `deband` + усиленный `unsharp` + upscale/downscale `lanczos`,
  - кодек/энкод усилен (`libx264`, `preset=veryslow`, `crf=14`, `tune=film`).
- API/settings/runtime расширены полем `enhance_ultra` (GET/POST `/api/settings`, defaults, runtime env).
- README обновлен: добавлены `W2L_ENHANCE_ULTRA` и новое поле в `POST /api/settings`.
- Обновлен cache-busting статики:
  - `styles.css?v=20260212_12`
  - `app.js?v=20260212_12`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно,
  - `python -m compileall Wav2LipViewer/app/main.py` успешно.
## 2026-02-12 (runtime UI regrouping: two collapses + actions below)
- В `Runtime Settings` добавлен второй сворачиваемый блок для базовых параметров (`Core runtime settings`):
  - в него перенесены поля от `Exec mode` до `No smooth`.
- Блок `Enhancements` оставлен как второй сворачиваемый блок.
- Под двумя сворачиваемыми блоками размещены:
  - `Preset`
  - `Apply preset`
  - `Save settings`.
- Из UI убрано упоминание `3090` у пресета `Maximum quality` (EN/RU + description).
- Обновлен cache-busting:
  - `styles.css?v=20260212_11`
  - `app.js?v=20260212_11`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (Enhancements UI switched to inline collapsible block)
- Убран modal-popup для улучшалок; вместо него добавлен встроенный сворачиваемый блок (`details/summary`) прямо в `Runtime Settings`.
- Внутри блока оставлены те же чекбоксы улучшалок и кнопка `Save enhancements`.
- Такой формат устойчивее в CEF и не зависит от overlay/modal-логики.
- Обновлен cache-busting:
  - `styles.css?v=20260212_10`
  - `app.js?v=20260212_10`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (hard fallback: inline onclick hooks for Enhancements modal)
- Для кнопок модалки добавлен прямой HTML fallback через `onclick`:
  - `openEnhanceModalBtn` вызывает `window.__w2lOpenEnhancements()`
  - `closeEnhanceModalBtn` вызывает `window.__w2lCloseEnhancements()`
- В `app.js` глобальные функции `window.__w2lOpenEnhancements` / `window.__w2lCloseEnhancements` привязаны к modal open/close.
- Обновлен cache-busting:
  - `styles.css?v=20260212_08`
  - `app.js?v=20260212_08`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (hotfix: Enhancements click fallback + manual CEF cache reset)
- Выполнена ручная очистка `Wav2LipViewer/app/data/cef_cache` для принудительного сброса CEF-кеша.
- В `Wav2LipViewer/app/web/app.js` добавлен fallback-обработчик кликов для modal-кнопок через `document` delegation:
  - `#openEnhanceModalBtn` всегда пытается открыть modal,
  - `#closeEnhanceModalBtn` всегда закрывает modal,
  - помогает, если основной bind в `init()` частично не сработал из-за рассинхрона статики.
- Обновлен cache-busting:
  - `styles.css?v=20260212_07`
  - `app.js?v=20260212_07`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (hotfix: Enhancements button not opening modal)
- В `Wav2LipViewer/app/web/app.js` усилена инициализация обработчиков для Enhancements modal:
  - все bind-операции на элементы модалки теперь с null-check,
  - добавлен fallback-message в `jobStatus`, если модалка недоступна из-за рассинхрона кеша/DOM.
- Открытие/закрытие модалки дополнительно управляет `style.display` (`flex/none`), чтобы убрать риск конфликтов с классом `hidden`.
- Обновлен cache-busting:
  - `styles.css?v=20260212_06`
  - `app.js?v=20260212_06`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (bundled FFmpeg for fully autonomous runtime)
- Скачана и встроена статическая сборка FFmpeg прямо в проект:
  - `Wav2LipViewer/app/bin/ffmpeg/ffmpeg.exe`
  - `Wav2LipViewer/app/bin/ffmpeg/ffprobe.exe`
  - `Wav2LipViewer/app/bin/ffmpeg/ffplay.exe`
- Backend `Wav2LipViewer/app/main.py` обновлен:
  - постпроцесс улучшалок теперь в приоритете использует локальный `app/bin/ffmpeg/ffmpeg.exe`,
  - если локальный бинарник отсутствует, fallback на `ffmpeg` из системного `PATH`.
- README обновлен: описано поведение bundled FFmpeg и fallback.
- Верификация:
  - `ffmpeg version 8.0.1-essentials_build-www.gyan.dev` из локальной папки,
  - `python -m compileall Wav2LipViewer/app/main.py` успешно.
## 2026-02-12 (enhancements modal + max quality preset + postprocess pipeline)
- В UI runtime settings добавлен отдельный стильный popup `Enhancements` с чекбоксами:
  - `Sharpen mouth region`
  - `Temporal denoise`
  - `Color and contrast match`
  - есть открытие/закрытие, сохранение, summary активных улучшалок.
- Добавлен новый пресет `Maximum quality (3090)` в `Runtime Preset`.
  - Пресеты теперь включают не только базовые Wav2Lip-параметры, но и состояние улучшалок.
- Backend `POST /api/settings` расширен новыми флагами:
  - `enhance_sharpen`
  - `enhance_denoise`
  - `enhance_color_boost`
  - они сохраняются в `runtime_settings.json` и участвуют в job runtime.
- В `JobRunner` добавлен реальный постпроцесс после успешного рендера:
  - при включенных улучшалках запускается `ffmpeg` pass (`hqdn3d`, `unsharp`, `eq`) и заменяет output-файл улучшенной версией,
  - в message jobs добавляется отметка, какие улучшалки были применены.
- Обновлен cache-busting:
  - `styles.css?v=20260212_05`
  - `app.js?v=20260212_05`.
- README обновлен по новым env/API полям улучшалок.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно,
  - `python -m compileall Wav2LipViewer/app/main.py` успешно.
## 2026-02-12 (jobs jitter reduction + cleaner jobs header + stronger HQ preset)
- В `Wav2LipViewer/app/web/index.html` очищен заголовок Jobs: убраны индикаторы `Queue: ...` и `q:l:r:d:f:c`, оставлена кнопка `Refresh`.
- В `Wav2LipViewer/app/web/app.js` снижены перескоки при polling jobs:
  - добавлен fingerprint списка задач (`jobsFingerprint`),
  - список jobs теперь перерисовывается только когда реально изменились данные задач,
  - сохранение скролла контейнера jobs сохранено.
- Усилен quality preset (`hq`) в runtime:
  - `face_det_batch=4`, `wav2lip_batch=24`, `pads="0 6 0 0"`, `resize_factor=1`, `nosmooth=0`.
  - Режим стал медленнее, но ориентирован на более качественный результат.
- Обновлен cache-busting:
  - `styles.css?v=20260212_04`
  - `app.js?v=20260212_04`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (probe UX polish: placeholder + auto frame refresh)
- В `Wav2LipViewer/app/web/index.html` и `styles.css` добавлен placeholder для блока Face Selection (`probeStage`):
  - при отсутствии видео/кадра вместо черного квадрата и битого `img` показывается аккуратная заглушка,
  - `probeFrame` скрывается через класс `is-empty`.
- В `Wav2LipViewer/app/web/app.js` добавлена функция `setProbeFrame(...)`:
  - централизованно переключает `probeFrame/placeholder`,
  - очищает face boxes/list при пустом кадре.
- Слайдер `Frame position` теперь обновляет кадр автоматически:
  - добавлен debounce (`~180ms`) на `input/change`,
  - `probeVideo()` вызывается без нажатия кнопки `Show frame and faces`.
- После upload видео автопревью перенастроено на первый кадр по сути (`~0.01s`), вместо 1 секунды.
- Обновлен cache-busting:
  - `styles.css?v=20260212_03`
  - `app.js?v=20260212_03`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (UX batch: auto-upload/probe, timeline end, presets, title bar cleanup)
- В `Wav2LipViewer/app/web/app.js` доработан flow загрузки видео:
  - выбор файла в `videoUploadInput` теперь автоматически запускает `uploadVideo()` без отдельного клика по кнопке,
  - после успешного upload автоматически выполняется probe на отметке 1 секунда (`frame_ratio = 1/duration`), и кадр сразу показывается в preview,
  - после загрузки/restore без сегментов `End` в timeline автоустанавливается на тайминг последнего кадра видео.
- В `Wav2LipViewer/app/web/app.js` улучшена стабильность скролла jobs:
  - убрано принудительное восстановление глобального scroll страницы,
  - сохраняется только scroll контейнера jobs, чтобы убрать визуальные перескоки.
- В runtime settings добавлены пресеты с описаниями и кнопкой применения:
  - `Balanced quality`, `Fast preview`, `High quality stable`,
  - для каждого пресета показывается пояснение, что дает режим (скорость/качество/нагрузка).
- В title bar убраны подписи `Multi-face pipeline` и `Lang` (оставлен только select EN/RU и кнопки окна).
- В `styles.css` стилизована кнопка `Choose file` через `::file-selector-button` (+ webkit fallback).
- Обновлен cache-busting:
  - `styles.css?v=20260212_02`
  - `app.js?v=20260212_02`.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно.
## 2026-02-12 (hotfix: white window compatibility + maximize keeps taskbar)
- В `Wav2LipViewer/app/web/app.js` смягчен механизм автообновления jobs для совместимости:
  - убраны `closest(...)` и `requestAnimationFrame(...)` из критического пути refresh,
  - сохранение/восстановление скролла переведено на более совместимый `parentNode + scrollTop`.
- В `Wav2LipViewer/app/launcher.py` переделан `maximize`:
  - вместо `ShowWindow(SW_MAXIMIZE)` добавлен кастомный toggle в `rcWork` (рабочая область монитора),
  - окно разворачивается без перекрытия панели задач (taskbar),
  - повторный maximize возвращает окно в сохраненный предыдущий размер/позицию.
- Верификация:
  - `node --check Wav2LipViewer/app/web/app.js` успешно,
  - `python -m compileall Wav2LipViewer/app/launcher.py` успешно.
## 2026-02-12 (title bar alignment + jobs progress UI + scroll stability)
- В `Wav2LipViewer/app/web/index.html` переработан блок `window-actions`:
  - язык и системные кнопки окна выровнены по одной горизонтальной линии в title bar,
  - текстовые символы `- [] x` заменены на SVG-иконки из `assets/icons` (`minimize.svg`, `maximize.svg`, `close.svg`),
  - обновлен cache-busting:
    - `styles.css?v=20260212_01`
    - `app.js?v=20260212_01`.
- В `Wav2LipViewer/app/web/styles.css`:
  - добавлено стабильное выравнивание `lang-control/lang-select` и `window-icon`,
  - стилизован scrollbar для интерфейса (track/thumb/hover),
  - добавлены стили progress bar в jobs (`.job-progress-*`) и контейнера действий (`.job-actions`).
- В `Wav2LipViewer/app/web/app.js`:
  - добавлен i18n-ключ `jobs.progress` (EN/RU),
  - реализован прогресс-бар в карточках jobs (читает `job.progress`, при отсутствии использует fallback по статусу),
  - `refreshJobs(...)` обновлен с сохранением позиции скролла при автообновлении jobs, чтобы UI не сбрасывался вниз.
- В backend `Wav2LipViewer/app/main.py` добавлено поле `progress` в lifecycle задач:
  - `queued/requeue` -> `progress=0`,
  - `running` -> прогресс по этапам,
  - terminal статусы (`done/failed/canceled`) -> `progress=100`,
  - manual worker flow (`leased/complete/fail`) также обновляет `progress`.
- Верификация:
  - `python -m compileall Wav2LipViewer/app/main.py` выполнен успешно.
## 2026-02-11 (i18n dictionary + EN/RU switch)
- Исправлена совместимость со старым CEF Chromium: удален оператор `??` из `app.js` (функция `t()`), чтобы исключить ранний JS parse error; обновлен cache-busting до `app.js?v=20260211_12`.`r`n- Добавлен hardening взаимодействия в шапке UI: drag больше не перехватывает элементы `.window-actions`, для `langSelect` добавлены обработчики `change` + `input`, для `windowAction` добавлен fallback `window.close()` при недоступном API; cache-busting `app.js?v=20260211_11`.`r`n- Исправлено переключение языка: в `I18N` добавлены отсутствующие ключи из `index.html` (runtime/video/face/tracking/timeline/audio/jobs), теперь `EN/RU` реально меняет подписи интерфейса.- Устранены проблемы с битой кодировкой UI за счет выноса текстов в словарь в `Wav2LipViewer/app/web/app.js` (`I18N`).
- Добавлен переключатель языка `EN/RU` в заголовке окна (`#langSelect`) и сохранение выбора в `localStorage` (`w2l_lang`).
- Добавлено применение переводов по ключам через `data-i18n`, `data-i18n-title`, `data-i18n-placeholder` (`Wav2LipViewer/app/web/index.html` + `applyStaticI18n()` в `app.js`).
- Основные статусы и кнопки переведены на словарную модель; динамические сообщения больше не зависят от локальной кодировки HTML.
- Обновлен cache-busting JS:
  - `app.js?v=20260211_10`.

## 2026-02-11 (runtime settings: full Wav2Lip controls in UI)
- Расширены runtime-настройки backend в `Wav2LipViewer/app/main.py`:
  - `POST /api/settings` теперь принимает и сохраняет параметры:
    - `checkpoint_path`
    - `use_box`
    - `face_det_batch`
    - `wav2lip_batch`
    - `pads`
    - `resize_factor`
    - `nosmooth`
  - Добавлена валидация/нормализация:
    - числовые поля ограничиваются допустимыми диапазонами,
    - `pads` нормализуется в формат `top bottom left right` (4 целых),
    - bool-поля приводятся к стабильному виду.
- Обновлен UI `Wav2LipViewer/app/web/index.html`:
  - в шаге `Runtime Settings` добавлены отдельные контролы для всех ключевых Wav2Lip-параметров.
- Обновлен фронтенд `Wav2LipViewer/app/web/app.js`:
  - `refreshSettings()` загружает и отображает новые параметры,
  - `saveSettings()` сохраняет новые параметры через `/api/settings`.
- Обновлен cache-busting JS:
  - `app.js?v=20260211_09`.
- README обновлен: зафиксировано, что расширенные Wav2Lip-параметры управляются из UI и перечислены в `POST /api/settings`.

## 2026-02-11 (video metadata + timeline normalization)
- Добавлен сбор метаданных видео при загрузке в `Wav2LipViewer/app/main.py`:
  - `fps`, `frame_count`, `duration_sec`, `width`, `height` сохраняются в `video_index`.
- Добавлен API:
  - `GET /api/video/meta?video_id=...`
- Усилена серверная валидация таймлайна в `POST /api/timeline/save`:
  - сегменты сортируются по времени,
  - обрезаются по длительности видео,
  - для пересечений между разными спикерами выполняется trim второго сегмента,
  - пересекающиеся/соседние сегменты одного спикера склеиваются,
  - в ответе возвращается статистика нормализации (`input_count`, `saved_count`, `dropped_invalid`, `adjusted_overlap`, `merged_same_speaker`).
- UI (`Wav2LipViewer/app/web/app.js`) обновлен:
  - после upload показываются метаданные видео,
  - при добавлении сегмента `start/end` ограничиваются длительностью ролика,
  - после сохранения таймлайна UI подхватывает нормализованные сегменты и показывает статистику нормализации.
- README обновлен: добавлен `GET /api/video/meta` и уточнение поведения `POST /api/timeline/save`.

## 2026-02-11 (UI context restore on restart)
- В `Wav2LipViewer/app/web/app.js` добавлено сохранение последнего `video_id` в `localStorage` (`w2l_last_video_id`) после успешной загрузки видео.
- На старте приложения добавлено восстановление контекста пайплайна по сохраненному `video_id`:
  - `GET /api/video/meta`
  - `GET /api/face/selection`
  - `GET /api/tracking`
  - `GET /api/timeline`
- После восстановления UI автоматически подхватывает:
  - метаданные видео,
  - выбранное target-лицо,
  - трекинг,
  - сегменты таймлайна (и заполняет `Speaker face_id` при наличии selection).
- Если сохраненный `video_id` недоступен (удален/очищен), UI очищает ключ и показывает диагностическое сообщение вместо падения.

## 2026-02-11 (reset session + speaker validation + probe restore)
- В UI добавлена кнопка `Reset session` (шаг Video):
  - очищает `localStorage` ключ `w2l_last_video_id`,
  - сбрасывает локальное состояние (`videoId`, `videoMeta`, selection/tracking/timeline, probe frame/boxes, input поля).
- В `Wav2LipViewer/app/web/app.js` улучшено восстановление контекста:
  - после восстановления `video_id` автоматически выполняется `POST /api/video/probe` по `selection.frame_ratio` (или `0.5`),
  - probe-кадр и face boxes загружаются сразу после перезапуска UI.
- На backend в `POST /api/timeline/save` добавлена валидация `speaker_face_id`:
  - принимаются только пустое значение или `face_id` выбранного target-лица для данного `video_id`,
  - при неверных значениях API возвращает `400` с `invalid_speaker_face_ids` и `allowed_speaker_face_ids`.
- README обновлен под новое поведение (`Reset session`, speaker validation в timeline save).
- Для `Reset session` в UI добавлено подтверждение через `confirm()`, чтобы избежать случайного сброса состояния.

## 2026-02-11 (responsive scaling fix)
- Переработан responsive-layout в `Wav2LipViewer/app/web/styles.css` для корректного масштабирования интерфейса:
  - главная сетка `layout` переведена на `minmax(...)` колонки с безопасным переключением в 1 колонку,
  - добавлены `min-width: 0` для карточек/шагов/лейблов/инпутов (устранены переполнения и выталкивание контента),
  - `timeline-add` переведен на `auto-fit` сетку вместо фиксированных 4 колонок,
  - `probe-row` и `tracking-row` корректно схлопываются в 1 колонку на узких окнах,
  - `jobs-head` и правая часть заголовка jobs получили `flex-wrap`,
  - `probe-stage` получил ограничение по высоте и `object-fit: contain` для предсказуемого масштаба кадра.
- Добавлены дополнительные брейкпоинты `@media (max-width: 1280px)` и `@media (max-width: 640px)` для small-window режима.
- Обновлен cache-busting CSS в `Wav2LipViewer/app/web/index.html` до `styles.css?v=20260211_05`.

## 2026-02-11 (output open + probe face selection fix)
- Исправлена проблема `Open result` в CEF (черное окно при попытке встроенного воспроизведения mp4):
  - добавлен backend endpoint `POST /api/output/open` в `Wav2LipViewer/app/main.py`,
  - endpoint открывает итоговый файл через `os.startfile(...)` во внешнем системном плеере.
- В списке jobs (`Wav2LipViewer/app/web/app.js`) блок результата обновлен:
  - кнопка `Open in player` вызывает `POST /api/output/open` для конкретного `job_id`,
  - отдельная ссылка `Download` оставлена для скачивания файла.
- Исправлена регрессия выбора лиц в probe-stage после responsive-изменений:
  - в `Wav2LipViewer/app/web/styles.css` возвращено корректное масштабирование кадра (`img { width: 100%; height: auto; }`),
  - убрано ограничение, ломающее геометрию overlay face-box относительно кадра.
- Обновлен cache-busting статики:
  - `styles.css?v=20260211_06`
  - `app.js?v=20260211_05`.

## 2026-02-11 (job cancel/delete + probe faces fallback)
- Добавлены API управления задачами:
  - `POST /api/job/cancel` (`job_id`) — отмена queued/leased задач (running не отменяется безопасно),
  - `POST /api/job/delete` (`job_id`) — удаление задачи (кроме running/leased) с очисткой `audio/output/temp` файлов.
- В `GET /api/jobs` добавлена статистика статуса `canceled`.
- В UI jobs (`Wav2LipViewer/app/web/app.js`) добавлены кнопки:
  - `Cancel` для `queued/leased`,
  - `Delete` для `queued/done/failed/canceled`.
- Для выбора лица добавлен fallback-список найденных лиц под probe-кадром:
  - новый блок `#probeFacesList` в `index.html`,
  - кнопки-лица (`face_id + bbox`) в `app.js`, выбор работает даже если overlay визуально неудобен.
- Для блока результата jobs:
  - сохранена кнопка `Open in player` (через backend `/api/output/open`),
  - добавлена ссылка `Download`.
- Обновлен cache-busting:
  - `styles.css?v=20260211_07`
  - `app.js?v=20260211_06`.

## 2026-02-11 (probe visual labels on-frame)
- Улучшена визуализация лиц прямо на кадре в шаге probe:
  - цветные рамки по каждому лицу,
  - контрастный `face_id` бейдж поверх рамки,
  - активное (выбранное) лицо подсвечивается отдельно.
- Список лиц под кадром синхронизирован с overlay:
  - у элементов списка такой же цвет, как у рамки на кадре,
  - активный элемент списка выделяется,
  - клик по рамке или по пункту списка выбирает одно и то же лицо.
- После выбора лица `selectFace(...)` теперь сразу перерисовывает overlay, чтобы было видно, какое лицо выбрано.
- Обновлен cache-busting:
  - `styles.css?v=20260211_08`
  - `app.js?v=20260211_07`.

## 2026-02-11 (probe bbox alignment hotfix)
- Исправлено смещение рамок лиц относительно изображения в probe-stage:
  - overlay теперь позиционируется в пикселях по фактическому размеру отрисованного кадра (`probeFrame.clientWidth/clientHeight`), а не по относительным % контейнера,
  - это устраняет разъезд рамок при изменении размера окна и при несоответствии высоты контейнера.
- Восстановлен пересчет overlay после загрузки кадра (`img.onload`) и при `window.resize`.
- Обновлен cache-busting:
  - `app.js?v=20260211_08`.

## 2026-02-11 (checkpoint EOF fallback + dropdown artifacts)
- В `Wav2LipViewer/app/workers/wav2lip_runner.py` добавлен fallback для ошибки checkpoint `unexpected EOF`:
  - если основной `wav2lip_gan.pth` падает с EOF, runner автоматически ретраит запуск с `Wav2Lip/checkpoints/wav2lip.pth`,
  - при успешном ретрае задача продолжает выполнение без ручного редактирования настроек.
- Для снижения черных артефактов в CEF на выпадающих списках/контекстных элементах:
  - в `styles.css` убран `backdrop-filter` из `.window-bar` и оставлен непрозрачный фон,
  - для `select`/`option` задан явный непрозрачный фон и цвет текста, добавлен `appearance` reset.
- Обновлен cache-busting CSS:
  - `styles.css?v=20260211_09`.

## 2026-02-11 (checkpoint integrity diagnosis)
- Выполнена прямая проверка checkpoint через embedded Python (`torch.load`):
  - `Wav2Lip/checkpoints/wav2lip_gan.pth` -> `RuntimeError: unexpected EOF`,
  - `Wav2Lip/checkpoints/wav2lip.pth` -> `RuntimeError: unexpected EOF`.
- Вывод: оба checkpoint-файла повреждены/неполные, ошибка не связана с входным видео.
- В `app/workers/wav2lip_runner.py` улучшена диагностика:
  - при `unexpected EOF` runner возвращает явный hint о необходимости перекачать checkpoint и показывает текущий путь `W2L_CHECKPOINT_PATH`,
  - если старт был с `wav2lip_gan.pth`, в сообщении отражается, что fallback на `wav2lip.pth` тоже был попытан.

## 2026-02-11 (checkpoint re-download completed)
- Перекачаны checkpoint-файлы `Wav2Lip/checkpoints/wav2lip_gan.pth` и `Wav2Lip/checkpoints/wav2lip.pth` из альтернативного release-источника.
- Выполнена валидация через embedded runtime (`torch.load`):
  - оба файла успешно читаются (`LOAD_OK`) и содержат ожидаемые ключи checkpoint.
- После замены checkpoint ошибка `RuntimeError: unexpected EOF ... checkpoint might be corrupted` должна быть устранена для новых/перезапущенных jobs.

## 2026-02-11 (lipsync visibility tuning defaults)
- Выявлено, что последний `done` job фактически выполнился, но lipsync визуально слабый/незаметный.
- Изменены дефолты запуска на более практичные для заметного lipsync:
  - `W2L_CHECKPOINT_PATH` по умолчанию переключен на `checkpoints/wav2lip.pth` (в `only_gpu.bat`, `debug_gpu.bat`, `set_wav2lip_env.example.bat`),
  - добавлен env-флаг `W2L_USE_BOX` (default `0`): по умолчанию runner **не** фиксирует `--box` из одного кадра, а позволяет face-detector сопровождать лицо по кадрам.
- В `wav2lip_runner.py` добавлен аргумент `--use-box` (привязан к `W2L_USE_BOX`), чтобы вручную можно было вернуть старое поведение (`W2L_USE_BOX=1`) для кейсов с несколькими лицами.

## 2026-02-11 (wav2lip face-select + timeline)
- Реализован новый backend flow под file-based Wav2Lip: upload video -> probe -> select face -> save timeline -> submit job.
- Добавлены API:
  - POST /api/video/upload
  - POST /api/video/probe
  - POST /api/face/select
  - GET /api/face/selection
  - POST /api/timeline/save
  - GET /api/timeline
- Job submit переведен на связку video_id + audio и требует выбранное target face.
- В job snapshot сохраняются target_face и timeline, чтобы worker рендерил по зафиксированной разметке.
- Worker расширен передачей target_json и timeline_json в шаблон команды W2L_INFER_CMD.
- UI переработан под пошаговый pipeline с выбором лица на кадре и ручной разметкой сегментов таймлайна.
- Добавлена валидация: без video_id, target face или audio job не создается.
- Выполнен smoke-тест API через Flask test client: upload/select/timeline/submit успешны.
- В текущем окружении probe backend = unavailable, потому что установка opencv-python блокируется proxy/network.
- Выполнен workaround через PowerShell + офлайн wheel install в embedded runtime:
  - скачаны `opencv_python-4.8.1.78-cp37-abi3-win_amd64.whl` и `numpy-1.24.4-cp38-cp38-win_amd64.whl` в `wheels/`,
  - установлены в `Wav2LipViewer/app/python` через `pip --isolated --no-index --find-links`,
  - `GET /api/config` теперь возвращает `probe_backend=opencv_haar`.

## 2026-02-11
- Копия проекта очищена от FaceID-специфичных модулей и данных, папка переименована в Wav2LipViewer.
- Сохранены reusable части: embedded runtime, CEF launcher-подход, web assets.
- Собран новый backend-каркас Wav2LipViewer/app/main.py под Wav2Lip workflow.
- Добавлены: загрузка пары video+audio, jobs store, очередь и фоновый worker.
- Добавлены статусы job: queued/running/done/failed.
- Реализованы режимы: stub по умолчанию и command через переменную W2L_INFER_CMD.
- Добавлен endpoint GET /api/config (режим, command_configured, queue_size).
- UI обновлен под новый pipeline: режим, очередь, автообновление jobs.
- Embedded Python очищен от неактуальных FaceID/ONNX/OpenCV зависимостей; оставлен минимальный runtime для Flask + CEF.
- README обновлен инструкцией по запуску inference через W2L_INFER_CMD.

## 2026-02-11 (smart tracking stage)
- Добавлен backend smart-tracking выбранного лица в `Wav2LipViewer/app/main.py`:
  - новый store `app/data/face_tracks.json`,
  - `FaceTrackerEngine` (sampled tracking на основе Haar detections + bbox matching по IoU/центру/площади),
  - API `POST /api/tracking/build` и `GET /api/tracking`.
- В `POST /api/job/submit` добавлена обязательная проверка построенного трека; без трекинга job не создается.
- Worker сохраняет `target_track.json` для каждой задачи и прокидывает путь в шаблон команды как `{track_json}`.
- UI обновлен:
  - шаг `Smart Tracking target-лица` (sample step + кнопка построения),
  - отображение статистики трека (points/coverage/step),
  - блокировка submit без построенного трека.
- README обновлен:
  - добавлены `{track_json}` и API `/api/tracking/*`.
- Выполнены проверки:
  - compileall для `app/main.py`, `app/launcher.py`, `app/web`,
  - end-to-end smoke test (синтетическое mp4 через OpenCV): `upload -> probe -> select -> tracking -> timeline -> submit` успешен.

## 2026-02-11 (runtime settings + worker api)
- Добавлены runtime-настройки рендера в `app/data/runtime_settings.json`:
  - `exec_mode` (`local` или `manual`),
  - `infer_command`,
  - `timeout_sec`.
- Добавлены API:
  - `GET /api/settings`
  - `POST /api/settings`
  - `POST /api/job/requeue`
  - `POST /api/worker/claim`
  - `POST /api/worker/complete`
  - `POST /api/worker/fail`
- В `manual` режиме backend больше не запускает local worker автоматически; задачи остаются в `queued` для внешних воркеров.
- В `local` режиме сохранено прежнее поведение (очередь + встроенный worker).
- `JobRunner` теперь запускает задачу только если статус действительно `queued` (защита от повторного выполнения).
- В UI добавлен шаг `Runtime Settings` (exec mode, timeout, command template) и отображение job-статистики.
- В UI добавлена кнопка `Requeue` для `failed/leased` задач.
- README обновлен описанием worker API и настроек выполнения.
- Smoke checks:
  - `GET/POST /api/settings` успешны,
  - `manual` flow с воркером: `claim -> complete -> job status done` успешен,
  - после тестов настройки возвращены в `exec_mode=local`, `infer_command=''`.

## 2026-02-11 (real inference runner integration)
- Добавлен встроенный runner `Wav2LipViewer/app/workers/wav2lip_runner.py`:
  - запускает официальный `inference.py` из внешнего Wav2Lip repo,
  - принимает метаданные пайплайна (`video/audio/output/target_json/track_json/timeline_json`),
  - использует bbox выбранного target face для `--box`,
  - поддерживает тюнинг через env (`W2L_FACE_DET_BATCH`, `W2L_BATCH`, `W2L_PADS`, `W2L_RESIZE_FACTOR`, `W2L_NOSMOOTH`).
- Добавлен шаблон запуска в README для поля `Runtime Settings -> Command template`:
  - `{app}\\python\\python.exe {app}\\workers\\wav2lip_runner.py ...`
- Добавлен `set_wav2lip_env.example.bat` для быстрого старта с `W2L_REPO_DIR` и `W2L_CHECKPOINT_PATH`.
- Выполнены проверки:
  - `python app/workers/wav2lip_runner.py --help` успешен,
  - compileall для `app/workers/wav2lip_runner.py`, `app/main.py`, `app/launcher.py` успешен.

## 2026-02-11 (Wav2Lip assets + deps bootstrap)
- Скачан официальный репозиторий `Wav2Lip` в `C:/Data/MyProjects/wav2lip/Wav2Lip`.
- Скачаны веса:
  - `Wav2Lip/checkpoints/wav2lip_gan.pth`,
  - `Wav2Lip/checkpoints/wav2lip.pth`,
  - `Wav2Lip/face_detection/detection/sfd/s3fd.pth`.
- В launch bat-файлы `Wav2LipViewer` добавлен автоподхват путей:
  - `W2L_REPO_DIR=%~dp0..\\Wav2Lip`,
  - `W2L_CHECKPOINT_PATH=%~dp0..\\Wav2Lip\\checkpoints\\wav2lip_gan.pth`.
- В runtime settings выставлен рабочий command template на `app/workers/wav2lip_runner.py`; `api/config` теперь показывает `mode=command`.
- В embedded runtime офлайн установлены зависимости для реального `inference.py`:
  - `torch 2.4.1+cpu`, `torchvision 0.19.1+cpu`, `scipy`, `librosa`, `numba`, `llvmlite`, `scikit-learn`, `tqdm` и сопутствующие пакеты.
- Патч совместимости в `Wav2Lip/audio.py`:
  - `load_wav()` переведен на `wavfile/ffmpeg` (без `librosa.load`),
  - обновлен вызов `librosa.filters.mel(...)` под новый API (`sr=..., n_fft=...`).
- Патч совместимости runner:
  - `wav2lip_runner.py` запускает `inference.py` через `runpy` с явным `sys.path` для embedded Python (`python38._pth` сценарий).
- Smoke-run реального inference доведен до стадии `datagen` (модель и чекпоинт грузятся; падение на synthetic тест-кейсе из-за пустого face crop ожидаемо).

## 2026-02-07
- Прочитано и разобрано ТЗ из `FaceID_Viewer_TZ.txt`.
- Подтверждён стек: Python + CEF + OpenCV + ONNX Runtime.
- Подтверждены основные модули: видеовход, детекция, распознавание, база людей, UI, логи.
- Зафиксировано требование к портативной сборке (без установки, относительные пути, CPU/GPU режимы).
- Создан каркас проекта `FaceIDViewer/` по структуре ТЗ.
- Реализован backend `FaceIDViewer/app/main.py`:
  - API управления источником и запуском видео,
  - MJPEG стрим для live-view,
  - детекция лиц (OpenCV Haar cascade),
  - базовое распознавание по локальным эмбеддингам,
  - хранение людей и эмбеддингов в `app/data/`.
- Реализован launcher `FaceIDViewer/app/launcher.py`:
  - запуск через CEF (`cefpython3`) при наличии,
  - fallback в обычный браузер при отсутствии CEF.
- Реализован UI `FaceIDViewer/app/web/`:
  - вкладки Live / People / Settings / Logs,
  - отображение FPS, количества лиц, режима CPU/GPU,
  - добавление/удаление людей, просмотр логов.
- Добавлены скрипты запуска `only_cpu.bat` и `with_gpu.bat`.
- Добавлен скрипт установки зависимостей `install_requirements.bat`.
- Добавлен `FaceIDViewer/README.md` с инструкцией запуска.
- Добавлен portable runtime `FaceIDViewer/app/python` (embedded Python 3.8.10, совместимый профиль для Windows 7+).
- Добавлены установщики embedded runtime:
  - `FaceIDViewer/setup_embedded_python.bat`
  - `FaceIDViewer/setup_embedded_python.ps1`
- Скрипты `only_cpu.bat`, `with_gpu.bat`, `install_requirements.bat` переключены на `app\\python\\python.exe`.
- Добавлен `FaceIDViewer/only_gpu.bat` как основной GPU-скрипт запуска.
- `with_gpu.bat` оставлен как совместимый алиас и вызывает `only_gpu.bat`.
- Удалён устаревший `with_gpu.bat` (оставлен единый основной GPU-скрипт `only_gpu.bat`).
- Добавлены debug-скрипты с консолью:
  - `debug_cpu.bat`
  - `debug_gpu.bat`
- Выполнен полный редизайн интерфейса под Spotify-style:
  - централизованный адаптивный layout (горизонтальное/вертикальное центрирование),
  - полностью кастомизированные контролы без стандартного WinUI вида,
  - локально подключённый шрифт `Roboto Condensed` (`app/web/assets/fonts/RobotoCondensed-wght.ttf`).
- Добавлен кастомный верхний бар окна внутри интерфейса:
  - кнопки `minimize / maximize / close` в UI,
  - нативный title bar скрыт на стороне CEF/Win32.
- Добавлен backend API управления окном:
  - `POST /api/window/action` (`minimize|maximize|close`).
- Обновлены `launcher.py` и `main.py` для поддержки borderless-окна и window actions.
- Пользовательский сценарий запуска упрощён: для запуска не требуется установка, только `only_cpu.bat` или `only_gpu.bat`.
- Удалены dev-скрипты из корня релизной папки:
  - `install_requirements.bat`
  - `setup_embedded_python.bat`
  - `setup_embedded_python.ps1`
- Реализован ONNX-backend распознавания в `FaceIDViewer/app/main.py`:
  - автоподхват `app/models/face_embedding.onnx`,
  - fallback на MVP-эмбеддинг при отсутствии/ошибке ONNX-модели.
- Добавлены API-настройки порога матчинга:
  - `GET /api/settings`
  - `POST /api/settings` (`match_threshold` 0..1).
- UI обновлён:
  - отображение backend распознавания (`mvp`/`onnx`),
  - настройка `match_threshold` во вкладке Settings.
- Добавлен `FaceIDViewer/app/models/README.txt` с инструкцией по подключению ONNX-модели.
- Исправлен критический запускной баг:
  - `FaceIDViewer/app/launcher.py` теперь корректно добавляет `app/` в `sys.path`,
  - устранён `ModuleNotFoundError: No module named 'main'` при старте из `.bat`.
- Улучшены launch-скрипты:
  - `only_cpu.bat` и `only_gpu.bat` теперь показывают код ошибки и `pause` при аварийном выходе.
- Устранён запуск в браузере:
  - в embedded runtime установлен `cefpython3`,
  - `app/launcher.py` переведён на обязательный CEF-режим (без browser fallback),
  - приложение запускается как отдельное окно Windows.
- Скачана и подключена ONNX модель эмбеддингов:
  - `FaceIDViewer/app/models/face_embedding.onnx` (InsightFace model pack),
  - backend распознавания активирован как `onnx`.
- Для ONNX backend установлен более реалистичный дефолт порога:
  - `match_threshold=0.35` (если переменная окружения не задана).
- Переделана логика UI/видеопотоков:
  - отдельные вкладки `Camera` и `Video`,
  - в `Video` добавлены player-like контролы: `Load`, `Play`, `Pause`, `Stop`, `Seek`.
- Расширен backend для режима видеофайла:
  - `paused` состояние,
  - прогресс/позиция/длительность в `/api/status`,
  - новые API: `/api/play`, `/api/pause`, `/api/seek`.
- Добавлен нативный video file picker в UI:
  - файл загружается через `/api/video/upload`,
  - пользователь больше не вводит путь вручную.
- Переработана логика персон:
  - снято ограничение на количество фото,
  - поддержан выбор фотофайлов и папки с изображениями,
  - для каждой персоны строится centroid-модель эмбеддинга.
- Добавлена оптимизация производительности видеопайплайна:
  - детекция на уменьшенном кадре (`frame_scale`),
  - детекция не на каждом кадре (`detect_every_n`),
  - повторное использование распознавания между циклами детекции,
  - настройка качества MJPEG (`jpeg_quality`) и лимита лиц (`max_faces`).
- Добавлены переключатели показа нераспознанных лиц отдельно для вкладок:
  - `show_unknown_camera`,
  - `show_unknown_video`.
- В `requirements.txt` зафиксированы версии пакетов под профиль Python 3.8.
- Зависимости установлены внутрь embedded runtime; системный Python для запуска проекта больше не требуется.

## Текущий статус
- Этап: MVP готов к запуску на embedded Python.
- Следующий этап: улучшить качество распознавания, заменив MVP-эмбеддинги на ONNX-модель.

## Следующие шаги
1. Провести ручное UX-тестирование плеерного сценария на длинных видео (pause/seek/end-of-file).
2. Добавить ONNX-детектор лиц (с fallback), чтобы полностью уйти от Haar cascade.
3. Добавить валидацию качества изображений при добавлении человека (размер лица, резкость, освещенность).
4. Добавить базовую нормализацию/дедупликацию фото персоны (чтобы не раздувать базу похожими кадрами).
- Устранены проблемы плотной компоновки элементов в новом UI:
  - усилены отступы между соседними кнопками/контролами,
  - добавлены дополнительные отступы в title bar (индикатор/заголовок).
- Переработано поведение медиапанелей:
  - камера и видео масштабируются под размер панели (`object-fit: contain`),
  - переработан layout, чтобы убрать лишний скролл внутри вкладок Camera/Video.
- Добавлен fullscreen для видеоплеера:
  - кнопка `Fullscreen` во вкладке Video,
  - поддержка стандартного и webkit fullscreen API.
- Переработано перетаскивание окна:
  - добавлены API `GET /api/window/rect` и `POST /api/window/move`,
  - фронтенд перешёл на координатный drag (mousemove -> move),
  - старый нестабильный drag через одноразовый `SendMessage` больше не используется в UI.
- Улучшена интеграция borderless окна в launcher:
  - отключено скругление углов на уровне DWM (если поддерживается),
  - снижен риск чёрных артефактов в углах окна.
- Обновлены cache-busting версии фронтенда в `index.html` до `20260207_27`.
- Добавлено отдельное окно видеоплеера: маршрут `/player` + новая страница `app/web/player.html`.
- Реализован новый frontend плеера `app/web/player.js`:
  - локальные контролы окна плеера (`Pick/Play/Pause/Stop/Seek/Show Unknown`),
  - кнопка закрытия окна плеера,
  - поллинг статуса и синхронизация времени/seek с backend API.
- Логика кнопки `Player Window` во вкладке Video изменена:
  - вместо fullscreen внутри основного окна открывается отдельное окно `/player`.
- Выполнен полный restyle окна плеера под Material 3 в `app/web/styles.css`:
  - отдельные M3-компоненты (`m3-btn`, `m3-icon-btn`, `m3-player-*`),
  - карточная структура заголовка/контролов/seek/видео-стейджа,
  - отдельная кнопка Close внутри окна плеера.
- Cache busting обновлён до версии `20260207_28`.
- Окно `player` переработано по запросу: контролы воспроизведения и прогресс перенесены поверх видео (overlay), закреплены внизу кадра и всегда видимы.
- Обновлена структура `app/web/player.html` и M3-стили overlay в `app/web/styles.css`.
- Обновлён cache-busting окна плеера до `v=20260207_29`.
- Основная вкладка `Video` переведена на ту же модель, что и отдельное окно плеера:
  - контролы и прогресс перенесены в overlay поверх видео,
  - панель закреплена внизу кадра и всегда видима.
- Добавлена защитная обработка seek от падений:
  - frontend (`app.js`, `player.js`) валидирует и clamp-ит значение перед `/api/seek`,
  - seek ошибки теперь не пробрасываются в UI,
  - backend (`main.py`) проверяет `ratio` на finite и границы [0..1],
  - `VideoEngine.seek_ratio` безопасно обрабатывает невалидные значения.
- Обновлён cache-busting основного окна до `index/app.js v=20260207_30`.
- Исправлен критический сценарий seek во время воспроизведения:
  - seek больше не трогает `cv2.VideoCapture` из HTTP-потока,
  - введена очередь `pending_seek_frame_idx`, применение seek перенесено в поток `VideoEngine._loop`,
  - добавлена строгая валидация `ratio` (finite + clamp) в `/api/seek`.
- Добавлен API камер `GET /api/cameras` с probe индексов и fallback открытия (`CAP_DSHOW` -> default backend).
- В UI камеры добавлен dropdown выбора камеры + кнопка `Refresh`:
  - `cameraSelect`, `refreshCamerasBtn`, автоподхват активной камеры из `/api/status`.
- Полностью кастомизирован визуал прогресс-бара (`#videoSeek`, `#playerSeek`) через `::-webkit-slider-*` без нативного WinAPI вида.
- Для доп. окна плеера добавлено принудительное снятие системного title bar для всех окон процесса:
  - `launcher.py` теперь периодически делает `EnumWindows` + borderless-стилизацию окон текущего процесса.
- Обновлён cache-busting до версии `20260207_31` в основном и дополнительном окнах.
- Убрана кнопка `Apply` для камер: выбор камеры теперь автоприменяется по изменению dropdown.
- В UI камеры добавлен выбор из списка с именами устройств (best-effort):
  - backend `/api/cameras` теперь возвращает имена устройств (Windows PnP query + fallback `Camera N`),
  - frontend синхронизирует выбранный источник камеры со статусом движка.
- Улучшено переключение источников:
  - при переключении на камеру источник сразу активируется,
  - при загрузке видео источник `file` сразу запускается без дополнительного шага и корректно переключается обратно на камеру.
- Расширены window API параметром `scope` (`main`/`active`) для поддержки popup окна:
  - `/api/window/action`, `/api/window/rect`, `/api/window/move`.
- Дополнительное окно плеера переработано под поведение основного окна:
  - добавлены кнопки `min/max/close`,
  - добавлен drag заголовка через `scope=active`.
- В `launcher.py` `WindowController` расширен поддержкой `scope=active` (foreground окно текущего процесса) для корректного управления popup.
- Обновлён cache-busting фронтенда до `v=20260207_32`.
- Исправлено сопоставление камер: основной путь выбора камеры переведён на ID вида `name:<device_name>` вместо чистого индекса, чтобы исключить перепутанные камеры при нескольких устройствах.
- `VideoEngine` теперь умеет открывать камеру по device name (`video=<name>`, `CAP_DSHOW`) с fallback на индекс.
- `GET /api/cameras` переработан:
  - сначала формирует список имён устройств,
  - затем проверяет доступность каждой камеры по имени,
  - только при неуспехе fallback на индексный probe.
- Исправлено переключение источников:
  - при выборе `camera` источник сразу стартует,
  - при загрузке видео через `/api/video/upload` источник `file` запускается сразу.
- Основное окно камер:
  - убрана кнопка `Apply`,
  - выбор камеры в dropdown применяется автоматически.
- Улучшено popup окно:
  - добавлены `min/max/close` и drag для дополнительного окна,
  - добавлена поддержка `scope=active` в window API,
  - popup получил рамку/периметр в стиле основного окна.
- В `launcher.py` усилено снятие системной рамки (включая EX styles), чтобы убрать белые/двойные артефакты края.
- В дополнительном окне добавлен режим просмотра камеры (переключатель `Camera/Video`, список камер, refresh) для поведения, аналогичного основному окну.
- Обновлён cache-busting до `v=20260207_33`.
- Исправлен критический баг `player.js`: обработчики `Camera/Video` в popup возвращены внутрь `initPlayer()`, устранён сломанный/частично неработающий JS.
- Добавлена изоляция вкладок `Camera` и `Video` в основном окне:
  - при переключении вкладки источник синхронизируется с вкладкой,
  - в `Video` без выбранного файла поток камеры больше не подмешивается (движок останавливается),
  - после выбора файла в `Video` источник автоматически переключается на файл.
- Улучшено отображение имён камер:
  - fallback индексных камер теперь подхватывает имена из списка устройств по позиции, если они найдены,
  - добавлены стили для `option` (`.input option`, `.m3-input option`) чтобы текст в dropdown всегда был виден.
- Обновлён cache busting до `v=20260207_35`.
- Popout разделён на два отдельных режима:
  - `Popout Camera` (из вкладки Camera) открывает `player?mode=camera&source=...`,
  - `Popout Video` (из вкладки Video) открывает `player?mode=video`.
- Popup больше не универсальный переключатель `Camera/Video`; поведение зависит от режима открытия окна.
- В camera-mode popup скрыты video-only элементы (seek/pick/pause), и окно стартует сразу с выбранной камерой из основной вкладки.
- Исправлено перепутывание названий в fallback-режиме камер:
  - удалён позиционный маппинг `device_names[idx] -> index`,
  - fallback теперь честно показывает `Camera N` вместо потенциально неверного имени.
- Уточнён смысл артефакта popup (правая/нижняя рамка): усилен borderless на Win32 уровне.
  - В `launcher.py` добавлен `WS_POPUP` и принудительный `SetWindowPos` с текущими габаритами + `SWP_FRAMECHANGED`.
- Добавлена очистка отображения при переключении источников:
  - backend хранит `blank_jpeg` и сбрасывает кадр на чёрный при `set_source()`/`stop()`,
  - frontend выполняет `resetStreamImage()` при смене camera/video источника.
- Popout окончательно разделён по режимам:
  - `Popout Camera` -> `player?mode=camera&source=...`,
  - `Popout Video` -> `player?mode=video`.
- Popup режим camera/video теперь не универсальный:
  - camera-mode скрывает video-only контролы (seek/pick/pause),
  - camera-mode стартует выбранную камеру из основного окна.
- По камерам убран риск ошибочного переименования в fallback:
  - убран позиционный маппинг device_names->index,
  - fallback показывает только `Camera N`.
- Обновлён cache busting до `v=20260207_37`.

- 2026-02-07 (popup/camera hotfix):
  - Подключен pygrabber (+ comtypes) в embedded Python для DirectShow-имен камер.
  - В pp/main.py добавлен _enumerate_windows_camera_names() (pygrabber -> PowerShell fallback).
  - Открытие камеры по 
ame:<device> усилено fallback-ом: если DSHOW-имя не открылось, пробуется индекс из перечисления.
  - Для индексных камер добавлена подпись из найденных имен устройств (если доступна).
  - Убраны артефакты размера popup: player-window-body/m3-player-shell переведены на 100% контейнера, minmax(0,1fr), подправлены отступы и stage sizing.
  - Обновлен cache-busting до =20260207_38, очищен pp/data/cef_cache.

- 2026-02-07 (camera mapping + popout borderless fix):
  - Убрана логика, способная перепутывать названия камер с индексами (fallback label снова Camera N без positional remap).
  - Для 
ame:<device> убран индексный fallback в _open_capture, чтобы не подменять выбранную камеру другой.
  - В launcher.py добавлено отключение DWM non-client rendering (DWMWA_NCRENDERING_POLICY=DWMNCRP_DISABLED) для борьбы с остаточным системным кантом popup справа/снизу.
  - Выполнены compileall и очистка pp/data/cef_cache.

- 2026-02-07 (camera names + popup borderless retry):
  - /api/cameras переведен на индексный список (id = индекс) с отображаемыми именами из DirectShow (pygrabber) по позиции.
  - Если индексные камеры недоступны, API отдает fallback-список 
ame:<device> чтобы имена не пропадали полностью.
  - Добавлен новый endpoint /api/window/borderless и проброс callback из launcher.py (WindowController.borderless).
  - В player.js добавлен принудительный вызов borderless для scope=active при старте popup и после maximize.
  - Обновлен cache-busting до =20260207_39, очищен pp/data/cef_cache.

- 2026-02-07 (reset approach):
  - В /api/cameras приоритет отдан прямым именам DirectShow (
ame:<device>) без принудительного index-remap, чтобы исключить перепутывание меток.
  - В _open_capture для 
ame:<device> оставлен DSHOW-open по имени + fallback на индекс устройства по позиции в DirectShow-списке.
  - В launcher.py для scope=active теперь берется корневое окно (GetAncestor(..., GA_ROOT)), чтобы borderless применялся к реальному top-level popup, а не к дочернему handle.
  - Прогнан compileall, очищен pp/data/cef_cache.

- 2026-02-07 (CEF popout from backend):
  - Реализован новый API /api/window/open_player в pp/main.py (mode=camera|video, source optional).
  - В launcher.py добавлен CEFWindowOpener: popout теперь создается через cef.CreateBrowserSync на UI-потоке (cef.PostTask), а не через window.open из JS.
  - Для нового CEF popup принудительно применяется borderless сразу и повторно через delayed tasks.
  - Кнопки Popout Camera/Popout Video в pp/web/app.js переведены на backend API открытия окна.
  - Убран автодобавляемый fallback-option в pp.js и player.js при 
efreshStatus (чтобы не появлялся лишний Camera 0 рядом со списком имен).
  - Обновлен cache-busting до =20260207_40, очищен pp/data/cef_cache.

- 2026-02-07 (pygrabber compatibility fix):
  - pygrabber downgraded from .2 to .1 for Python 3.8 compatibility in embedded runtime.
  - Verified FilterGraph().get_input_devices() works and returns camera names without crash.
  - Verified /api/cameras now returns named devices (
ame:<device> ids) instead of mixed fallback list.
  - Cleared pp/data/cef_cache before restart.

- 2026-02-07 (main window stream white fix):
  - В pp/web/app.js упрощен 
esetStreamImage: убрана промежуточная GIF-заглушка, теперь сразу переподключение к /api/stream?ts=....
  - Добавлен принудительный 
esetStreamImage('videoStream') после play/pause/stop для стабильного рендера потока в основном окне.
  - Обновлен cache-busting pp.js до =20260207_41, очищен pp/data/cef_cache.

- 2026-02-07 (settings input reset fix):
  - В pp/web/app.js добавлен guard от перезаписи полей настроек во время редактирования (focus-aware update).
  - 	hreshold и daptive_target_fps больше не сбрасываются поллингом, пока поле в фокусе.
  - Обновлен cache-busting pp.js до =20260207_42, очищен pp/data/cef_cache.

- 2026-02-07 (RU localization + window icons):
  - Интерфейс index.html и player.html переведен на русский (вкладки, кнопки, подписи, title/alt/tooltip).
  - В pp.js и player.js переведены пользовательские сообщения, алерты и статусы.
  - Добавлены локальные SVG-иконки оконных кнопок (pp/web/assets/icons/minimize.svg, maximize.svg, close.svg) из Bootstrap Icons.
  - Текстовые символы - [] x заменены на SVG-иконки во всех окнах.
  - Добавлен стиль .window-icon в styles.css для единого визуального вида.
  - Обновлен cache-busting до =20260207_43, очищен pp/data/cef_cache.

- 2026-02-07 (comment cleanup):
  - Удалены комментарии из рабочих исходников проекта: pp/main.py, pp/launcher.py, pp/web/app.js, pp/web/player.js, pp/web/styles.css.
  - Проверено поиском по шаблонам комментариев: совпадений в этих файлах не осталось.
  - Прогнан compileall для Python-файлов после очистки комментариев.

- 2026-02-07 (auth/login):
  - Добавлен модуль pp/auth_store.py для зашифрованной базы пользователей (pp/data/users.enc) и ключа (pp/data/auth.key).
  - Реализовано управление пользователями отдельным независимым скриптом manage_users.py (команды: init, list, set-password <user>, delete <user>).
  - В pp/main.py добавлены маршруты авторизации: /login, /api/auth/status, /api/auth/login, /api/auth/logout.
  - Введен efore_request-guard: без авторизации доступ к рабочим страницам и /api/* закрыт (кроме auth и оконных действий).
  - Добавлена страница входа pp/web/login.html и скрипт pp/web/login.js.
  - В главном окне добавлена кнопка Выйти (logout через /api/auth/logout).
  - Выполнена инициализация auth-хранилища: ключ и пустая база пользователей созданы.
  - Очищен pp/data/cef_cache.

- 2026-02-07 (user admin keyboard + bat):
  - В manage_users.py добавлен интерактивный клавиатурный режим (меню 1-5): инициализация, список, создать/обновить, удалить, выход.
  - При запуске без аргументов manage_users.py автоматически открывает интерактивное меню.
  - Добавлена команда CLI menu для явного запуска меню.
  - Создан manage_users.bat для запуска админки пользователей через embedded Python одним файлом.
  - Прогнан compileall для manage_users.py.

- 2026-02-07 (login fallback fix):
  - Добавлен серверный fallback-логин через POST /login (form submit), чтобы вход работал даже если JS логина не отработал.
  - В login.html форма переведена на method=post action=/login и добавлены 
ame у полей.
  - В login.js добавен вывод ошибок из query-параметра ?error=... (invalid, missing, db).
  - Проверены оба сценария входа: form login и API login — оба успешны.
  - Обновлен cache-busting для login-страницы до =20260207_45, очищен pp/data/cef_cache.

- 2026-02-07 (token auth, no cookies):
  - Авторизация переведена на без-cookie режим: в памяти процесса хранится только один активный токен/пользователь.
  - Доступ к /, /player и ко всем рабочим /api/* теперь только по токену (query 	oken или заголовок X-Auth-Token / Authorization: Bearer).
  - /api/auth/login возвращает 	oken; /api/auth/logout сбрасывает токен в памяти.
  - login.js после успешного входа делает redirect на /?token=... (без cookie).
  - pp.js и player.js добавляют токен во все API-запросы и требуют токен в URL при открытии страницы.
  - window.open_player теперь прокидывает токен в URL popout-окна (/player?...&token=...).
  - Проверен flow: без токена редирект на /login, с токеном доступ есть, после logout токен недействителен.
  - Обновлен cache-busting до =20260207_46, очищен pp/data/cef_cache.

- 2026-02-07 (UTF-8 recovery):
  - Полностью восстановлена русская локализация после сбоя кодировки в pp/web/index.html, pp/web/player.html, pp/web/login.html.
  - Исправлены битые русские строки в pp/web/login.js, pp/web/app.js, pp/web/player.js.
  - Обновлен cache-busting статики до =20260207_47 (HTML страницы).
  - Очищен FaceIDViewer/app/data/cef_cache для принудительной загрузки новых файлов.

- 2026-02-07 (stream window fix):
  - Исправлен layout контейнеров потока в pp/web/styles.css: добавлены min-width: 0, width/height: 100%, position: relative, overflow: hidden для media-panel, центровка и черный фон у stream images.
  - Устранены битые fallback-строки камер в pp/web/app.js и pp/web/player.js (Камера N вместо ??????).
  - Обновлен cache-busting до =20260207_48 в index.html, player.html, login.html и очищен pp/data/cef_cache.

- 2026-02-07 (broken stream icon fix):
  - Причина: img src=/api/stream не передавал auth-токен после перехода на без-cookie авторизацию.
  - В pp/web/app.js добавлен streamUrl() с query-параметром 	oken, 
esetStreamImage() переведен на него.
  - В pp/web/player.js добавлены streamUrl() и 
esetPlayerStream(), поток обновляется с токеном при старте и на play/pause/stop.
  - Обновлен cache-busting до =20260207_49, очищен pp/data/cef_cache.

- 2026-02-07 (manage_users relocate):
  - Скрипт управления пользователями перенесен из корня в FaceIDViewer/app/manage_users.py.
  - Обновлен путь запуска в FaceIDViewer/manage_users.bat на ./app/manage_users.py.
  - Внутри pp/manage_users.py скорректирован путь к базе/ключу: теперь используется pp/data относительно текущей папки скрипта.
  - Проверено: python -m compileall app/manage_users.py успешно.

- 2026-02-07 (README RU):
  - FaceIDViewer/README.md полностью переведен на русский язык.
  - Обновлены разделы: запуск, авторизация, управление пользователями, API, структура проекта и примечания.

- 2026-02-07 (technical PDF):
  - Сформирован технический документ на русском в корне проекта: FACEID_VIEWER_TECHNICAL_DESCRIPTION_RU.pdf.
  - Документ содержит назначение, архитектуру, стек, модель данных, API, запуск, безопасность и ограничения системы.

- 2026-02-07 (user manual PDF):
  - Добавлен подробный пользовательский мануал на русском: FACEID_VIEWER_USER_MANUAL_RU.pdf в корне проекта.
  - Добавлен скрипт генерации uild_user_manual_pdf.py для повторной пересборки инструкции.

- 2026-02-07 (model principles PDF):
  - Добавлен обзорный PDF о принципе работы модели в терминах математики и алгоритмов: FACEID_VIEWER_MODEL_PRINCIPLES_RU.pdf.
  - Документ отражает именно текущую реализацию: Haar-детектор, ONNX-эмбеддинг 512D (112x112), cosine similarity, centroid-модель персоны, threshold и MVP fallback.

- 2026-02-07 (startup video folder cleanup):
  - При старте приложения добавлена автоматическая очистка папки `FaceIDViewer/app/data/videos`.
  - Очищаются только файлы и подпапки внутри, сами папки сохраняются.

## Дальнейшие шаги
1. Прогнать smoke-тест: положить тестовый файл в `FaceIDViewer/app/data/videos`, запустить приложение и проверить, что папка очищается на старте.
2. При необходимости добавить флаг в настройки/ENV для отключения автоочистки на запуске.
























































