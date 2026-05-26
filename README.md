# DVR-Scan-File-Organizer

Dockerized batch wrapper for [DVR-Scan](https://www.dvr-scan.com/) that processes multiple videos and organizes output into `motion/` and `original/` folders.

## Stack

| Component | Version / detail |
|-----------|------------------|
| Language | Python 3.14 |
| Motion detection | `dvr-scan[opencv-headless]` |
| GPU (optional) | `cuda-core[cu13]` + `nvidia/cuda:13.2.1-cudnn-runtime-ubuntu24.04` |
| Lint / format | pylint 3.0.3, black 24.3.0 |
| Tests | pytest |
| Runtime | Docker (CPU default; optional CUDA image) |
| CI | GitHub Actions |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- For CUDA: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

## Setup

```sh
git clone https://github.com/derek-palmer/DVR-Scan-File-Organizer.git
cd DVR-Scan-File-Organizer
make build
```

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DVR_SCAN_CONFIG` | No | unset | Path to `dvr-scan.cfg`; `make run` sets `/config/dvr-scan.cfg` in the container |

DVR-Scan options live in [`dvr-scan.cfg`](dvr-scan.cfg). See the [DVR-Scan config docs](https://dvr-scan.readthedocs.io/en/latest/guide/config_file/).

Override at runtime:

```sh
export DVR_SCAN_CONFIG=/path/to/custom.cfg
make run
```

## Usage

Place input videos in `videos/` (`.mp4`, `.avi`, `.mkv`), then:

```sh
make run
```

Output layout:

```
output/
  motion/
    clip.mp4_motion.avi
  original/
    clip.mp4
```

### CLI (without Make)

```sh
docker run --rm -e PYTHONPATH=/app \
  -v "$(pwd)/videos:/videos" -v "$(pwd)/output:/output" \
  -v "$(pwd)/dvr-scan.cfg:/config/dvr-scan.cfg:ro" \
  -v "$(pwd)/dvr_scan_file_organizer:/app/dvr_scan_file_organizer" \
  dvr-scan-file-organizer \
  --input /videos --output /output --config /config/dvr-scan.cfg
```

Processor arguments: `--input` (required), `--output` (required), `--config` (optional).

### CUDA (optional)

```sh
make build-cuda
make run-cuda
```

CPU image is default; CI uses CPU only. Check [NVIDIA CUDA tags](https://hub.docker.com/r/nvidia/cuda/tags?name=cudnn-runtime-ubuntu) for newer base images; update `CUDA_IMAGE` in [`Dockerfile.cuda`](Dockerfile.cuda).

### Headless operation

No X11 or GUI: `opencv-headless`, FFmpeg in Docker, per [DVR-Scan headless guidance](https://www.dvr-scan.com/download/#servers-and-headless-systems).

## Testing

```sh
make test      # pytest in Docker
make lint      # pylint
make format    # black
make quality   # format + lint
```

Local venv (optional):

```sh
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/
```

## Documentation maintenance

This repo uses [codeforerunner](https://pypi.org/project/codeforerunner/) for scan-first doc updates:

```sh
source .venv/bin/activate   # after pip install -r requirements-dev.txt
forerunner scan             # prompt bundle → agent runs scan
forerunner doc readme       # refresh README from scan evidence
forerunner check            # drift rules (needs forerunner.config.yaml)
```

Latest scan artifact: [`docs/forerunner-scan.yaml`](docs/forerunner-scan.yaml).

## Project structure

```
DVR-Scan-File-Organizer/
├── dvr_scan_file_organizer/
│   ├── processor.py          # Batch scan CLI
│   └── organizer.py          # Output layout
├── tests/
├── docs/
│   ├── agents/               # Agent skill config
│   └── forerunner-scan.yaml  # Latest forerunner scan
├── videos/                   # Input (mounted at runtime)
├── output/                   # Output (mounted at runtime)
├── dvr-scan.cfg
├── forerunner.config.yaml
├── Dockerfile
├── Dockerfile.cuda
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── SPEC.md
├── AGENTS.md
└── README.md
```

## Summary

- Dockerized headless batch processing on Python 3.14
- Live-mounted volumes for fast dev iteration
- Structured output: motion clips + original copies
- Configurable via `dvr-scan.cfg` and optional CUDA profile
