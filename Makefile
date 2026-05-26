# Makefile - Optimized for Live Mounting (No Rebuild Needed)

.PHONY: help build build-cuda run run-cuda lint test clean scan format quality

CONFIG_MOUNT := -v $(PWD)/dvr-scan.cfg:/config/dvr-scan.cfg:ro
CONFIG_ENV := -e DVR_SCAN_CONFIG=/config/dvr-scan.cfg
CODE_MOUNTS := -v $(PWD)/dvr_scan_file_organizer:/app/dvr_scan_file_organizer \
	-v $(PWD)/tests:/app/tests
RUN_ARGS := --input /videos --output /output --config /config/dvr-scan.cfg

# Default help command
help:
	@echo "Available commands:"
	@echo "  make build       - Build the CPU Docker container"
	@echo "  make build-cuda  - Build the CUDA Docker container"
	@echo "  make run         - Run CPU container with input/output volume mapping"
	@echo "  make run-cuda    - Run CUDA container with GPU (--gpus all)"
	@echo "  make lint        - Run pylint inside the Docker container (no rebuild)"
	@echo "  make test        - Run pytest tests inside the Docker container (no rebuild)"
	@echo "  make scan        - Scan Docker image for vulnerabilities"
	@echo "  make clean       - Remove old images and cache"
	@echo "  make format      - Format Python files using Black"
	@echo "  make quality     - Run format and lint"

# Build the container (installs dependencies only)
build:
	docker build -t dvr-scan-file-organizer .

build-cuda:
	docker build -f Dockerfile.cuda -t dvr-scan-file-organizer-cuda .

# Run the container (mounts source code live)
run:
	docker run --rm -e PYTHONPATH=/app $(CONFIG_ENV) \
	-v $(PWD)/videos:/videos -v $(PWD)/output:/output \
	$(CONFIG_MOUNT) $(CODE_MOUNTS) \
	dvr-scan-file-organizer $(RUN_ARGS)

run-cuda:
	docker run --rm --gpus all -e PYTHONPATH=/app $(CONFIG_ENV) \
	-v $(PWD)/videos:/videos -v $(PWD)/output:/output \
	$(CONFIG_MOUNT) $(CODE_MOUNTS) \
	dvr-scan-file-organizer-cuda $(RUN_ARGS)

# Run linting inside a temporary container (no rebuild needed)
lint:
	docker run --rm -e PYTHONPATH=/app $(CODE_MOUNTS) \
	--entrypoint pylint dvr-scan-file-organizer dvr_scan_file_organizer tests

format:
	docker run --rm $(CODE_MOUNTS) \
	--entrypoint black dvr-scan-file-organizer /app/dvr_scan_file_organizer /app/tests

quality: format lint

# Run tests inside a temporary container (no rebuild needed)
test:
	docker run --rm -e PYTHONPATH=/app $(CODE_MOUNTS) \
	--entrypoint pytest dvr-scan-file-organizer /app/tests

clean:
	docker rmi -f dvr-scan-file-organizer dvr-scan-file-organizer-cuda || true
	docker builder prune -f --filter "label=project=dvr-scan-file-organizer"
