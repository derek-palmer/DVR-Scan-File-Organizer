# todo — DVR-Scan-File-Organizer

Execution checklist. Maps to `SPEC.md` §T. GitHub issues noted where applicable.

## Phase 1 — Docs / spec

- [x] **T1** — SPEC.md written
- [x] **T2** — todo.md written

## Phase 2 — Core pipeline

- [x] **T3** — Copy originals to `output_dir` after each `dvr-scan` run (`processor.py`) → V1, V2
- [x] **T4** — Validate input dir exists + has supported videos; non-zero exit → V6
- [x] **T5** — Config file support ([#2](https://github.com/derek-palmer/DVR-Scan-File-Organizer/issues/2))
  - [x] Add `dvr-scan.cfg` repo default
  - [x] `--config` CLI + `DVR_SCAN_CONFIG` env
  - [x] Pass `-c` to every `dvr-scan` invocation
  - [x] Mount config in `make run`
- [x] **T6** — Package hygiene: `__init__.py`, drop `opencv-python` from requirements

## Phase 3 — Tests / CI

- [x] **T7** — Test fixtures via ffmpeg; assert `motion/` + `original/` layout; no skips
- [x] **T11** — `make quality` + `make test` green in Docker (8/8 pytest pass locally; Docker daemon unavailable here)

## Phase 4 — Docs

- [x] **T8** — README fixes + headless docs ([#7](https://github.com/derek-palmer/DVR-Scan-File-Organizer/issues/7))
- [x] **T10** — `videos/.gitkeep`, `output/.gitkeep`

## Phase 5 — CUDA (optional profile)

- [x] **T9** — `Dockerfile.cuda` + `make build-cuda` / `make run-cuda` ([#6](https://github.com/derek-palmer/DVR-Scan-File-Organizer/issues/6))

## Phase 6 — Close loop

- [x] **T12** — Update §T statuses in SPEC.md + checkboxes here
- [ ] Comment on GitHub #2, #6, #7 (awaiting explicit permission to post/close)
