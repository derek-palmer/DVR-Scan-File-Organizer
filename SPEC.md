# SPEC — DVR-Scan-File-Organizer

## §G — Goal

Batch-run DVR-Scan on all videos in input dir. Organize output into `motion/` + `original/` subdirs. Docker-first workflow.

## §C — Constraints

- Python 3.14, Docker primary runtime
- Headless OpenCV (`dvr-scan[opencv-headless]`), no X11/GUI
- CPU default; optional CUDA profile separate from CI
- Issue tracker: GitHub (`derek-palmer/DVR-Scan-File-Organizer`) per `AGENTS.md`
- Supported input ext: `.mp4`, `.avi`, `.mkv`

## §I — Interfaces

| Surface | Detail |
|---------|--------|
| CLI | `--input`, `--output`, `--config` (optional) |
| Config | `dvr-scan.cfg` repo default; env `DVR_SCAN_CONFIG` override |
| Make | `build`, `run`, `test`, `lint`, `format`, `quality`, `build-cuda`, `run-cuda` |
| Output layout | `output/motion/{stem}_motion.avi`, `output/original/{basename}` |
| Entry | `python -m dvr_scan_file_organizer.processor` |

## §V — Invariants

- **V1** — Every processed input video → `motion/{stem}_motion.avi` exists after run
- **V2** — Every processed input video → `original/{basename}` exists (copy from input, input untouched)
- **V3** — `organize_output` only moves files in output root, not inside subdirs
- **V4** — When config path set, every `dvr-scan` call passes `-c <path>`
- **V5** — Default Docker image runs CPU/headless without display deps
- **V6** — Missing input dir or no supported videos → clear error, non-zero exit

## §T — Tasks

| id | status | task | cites |
|----|--------|------|-------|
| T1 | x | Write SPEC.md | — |
| T2 | x | Write todo.md | — |
| T3 | x | Copy originals to output_dir in processor | V1,V2 |
| T4 | x | Add input validation (missing dir, empty input) | V6 |
| T5 | x | Add dvr-scan.cfg + --config CLI + Makefile mount | V4,I.config |
| T6 | x | Add __init__.py; drop redundant opencv-python | V5 |
| T7 | x | Fix tests: ffmpeg fixture, motion/ + original/ asserts | V1,V2 |
| T8 | x | Fix README typos, structure, headless docs | V5,I |
| T9 | x | Add Dockerfile.cuda + make build-cuda/run-cuda | V5 |
| T10 | x | Add videos/.gitkeep, output/.gitkeep | — |
| T11 | x | Run make quality + make test green | V1–V6 |
| T12 | x | Update §T statuses + todo.md checkboxes | — |

## §B — Bugs

| id | date | cause | fix |
|----|------|-------|-----|
| B1 | 2026-05-25 | scan wrote motion files only; originals stayed in input dir so `original/` empty | V2; copy original to output_dir before organize |
| B2 | 2026-05-25 | `libgl1-mesa-glx` obsolete on Debian Trixie (python:3.14-slim) | use `libgl1` in Dockerfile + Dockerfile.cuda |
| B3 | 2026-05-25 | CUDA base pinned to 12.4.1; upstream at 13.2.1 | bump Dockerfile.cuda + `cuda-core[cu13]` |
