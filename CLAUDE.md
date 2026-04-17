# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MakeClip is an AI-powered worship video segmentation tool. It analyzes family worship videos/audio, segments them into 8-15 second clips, classifies each clip (praise/prayer/scripture/sermon), and assembles highlight reels.

**Language:** Python 3.14+ | **Domain:** Korean-language worship media processing

## Running the Pipeline

All scripts run from the repo root:

```bash
python split_video.py          # Analyze & segment all videos in media/ (WARNING: recreates media/output/)
python process_kakao.py        # Same analysis for KakaoTalk audio files (kakaotalk_*.m4a)
python rename_output.py        # Apply filename/folder mappings to video output
python rename_kakao.py         # Apply mappings to KakaoTalk output
python assemble_video.py       # Stitch clips into 3min reel → media/result/GeminiCLI/
python assemble_video_codex.py # Stitch clips into 3min reel → media/result/Codex/
```

**Dependencies:** `pip install openai-whisper moviepy librosa numpy torch`

**FFmpeg** is required and hardcoded to `C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin`. Update this path if your environment differs.

## No Automated Tests

There is no test suite. Validate changes manually:
- Check clip names and folder placement in `media/output/`
- Review `_summary.txt` files for correct transcription and ratio metrics
- Verify final renders in `media/result/`
- For segmentation/labeling logic changes, test at least one video AND one KakaoTalk audio file

## Architecture

This is a script-first media pipeline, not a packaged Python app. Entry points are top-level scripts.

### Core Classification Logic (V4) — `process_labels_prioritized_v4(chunks)`

Three-pass system with priority: **Praise > Prayer > Scripture > Sermon (default)**

1. **Praise** — ratio-based: harmonic/percussive energy ratio >= 3.0 to start, >= 2.0 to sustain
2. **Prayer** — context-based: regex detects start patterns (기도하시겠, 하나님아버지) and end patterns (예수님 이름으로 기도합니다/아멘); retroactively groups up to 2 prior chunks as prayer
3. **Scripture** — keyword-based: requires keywords (성경, 봉독, 말씀은) plus digit presence
4. **Sermon** — fallback for everything else

### Audio Analysis — `analyze_audio_raw()`

Uses Librosa HPSS (Harmonic-Percussive Source Separation) at 22050 Hz to compute the harmonic/percussive energy ratio that drives praise detection.

### Chunking Rules

Whisper segments accumulate until a sentence ending is detected (. ? ! 요 다 죠 오 아 아멘). Splits at 8-15 seconds on sentence boundaries, force-splits at >15 seconds. Clips under 1.5 seconds are skipped.

### Output Format

- Clips: `[family]_[seq]_[timestamp]_[label].mp4` (or `.m4a` for audio-only)
- Summaries: `[family]_summary.txt` with ratio metrics, timestamps, transcripts
- `media/output/` and `media/result/` are generated artifacts — do not store manual work there

## Coding Conventions

- 4-space indentation, `snake_case` everywhere
- Explicit `os.path` for filesystem paths (no `pathlib`)
- No formatter/linter configured — match adjacent code style
- Keep file naming patterns stable (e.g., `base_001_00m00s_label.mp4`)
- Whisper model: `medium`, language: `ko`, auto-detects CUDA
- Video output: H.264 (`libx264`), AAC audio, 1280x720 resolution

## Commit Style

Short imperative commits: `fix: preserve output naming during kakao rename`
