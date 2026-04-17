# Repository Guidelines

## Project Structure & Module Organization
This repository is a script-first media pipeline, not a packaged Python app. Core entry points live at the repo root:

- `split_video.py`: splits source videos in `media/` into labeled clips under `media/output/`
- `process_kakao.py`: runs the same analysis flow for Kakao audio files (`kakaotalk_*.m4a`)
- `rename_output.py` and `rename_kakao.py`: apply filename and folder mappings after processing
- `assemble_video.py`: stitches selected clips into `media/result/GeminiCLI/Worship_Gathering_3min.mp4`
- `GUIDE.md`, `CREATION_PROCESS.md`, and `STORYBOARD.md`: process notes and editorial context

Treat `media/output/` and `media/result/` as generated artifacts.

## Build, Test, and Development Commands
Use Python 3.14+ and install the runtime dependencies used by the scripts: Whisper, MoviePy, Librosa, NumPy, Torch, and FFmpeg.

```powershell
python split_video.py
python process_kakao.py
python rename_output.py
python rename_kakao.py
python assemble_video.py
```

Run from the repository root. `split_video.py` recreates `media/output/`, so do not keep anything there that is not disposable.

## Coding Style & Naming Conventions
Follow the existing style in the repository:

- 4-space indentation, top-level helper functions, and simple script entry points
- `snake_case` for functions, variables, and filenames
- keep file naming patterns stable, for example `base_001_00m00s_label.mp4`
- prefer explicit filesystem paths with `os.path`

No formatter or linter is configured in the repo. Keep edits small, readable, and consistent with adjacent code.

## Testing Guidelines
There is no automated test suite yet. Validate changes by running the affected script against sample files in `media/` and checking:

- generated clip names and folder placement
- summary text output in `media/output/*/*_summary.txt`
- final render output in `media/result/`

If you change segmentation or labeling logic, verify at least one video and one Kakao audio input.

## Commit & Pull Request Guidelines
The current workspace does not include `.git` history, so no repository-specific commit convention can be inferred. Use short imperative commits such as `fix: preserve output naming during kakao rename`.

For pull requests, include:

- a brief summary of the workflow change
- affected scripts and media paths
- manual verification steps and sample outputs
- screenshots only when UI-adjacent docs or rendered results need visual review

## Configuration Notes
The scripts assume FFmpeg is installed at `C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin`. If your environment differs, update that path before running the pipeline.
