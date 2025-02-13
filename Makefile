# Makefile - Optimized for Live Mounting (No Rebuild Needed)

.PHONY: help build run lint test clean scan format quality

# Default help command
help:
	@echo "Available commands:"
	@echo "  make build       - Build the Docker container"
	@echo "  make run         - Run the container with input/output volume mapping"
	@echo "  make lint        - Run pylint inside the Docker container (no rebuild)"
	@echo "  make test        - Run pytest tests inside the Docker container (no rebuild)"
	@echo "  make scan        - Scan Docker image for vulnerabilities"
	@echo "  make clean       - Remove old images and cache"
	@echo "  make format      - Format Python files using Black"
	@echo "  make quality     - Run format and lint"

# Build the container (installs dependencies only)
build:
	docker build -t dvr-scan-file-organizer .

# Run the container (mounts source code live)
run:
	docker run --rm -e PYTHONPATH=/app \
	-v $(PWD)/videos:/videos -v $(PWD)/output:/output \
	-v $(PWD)/dvr_scan_file_organizer:/app/dvr_scan_file_organizer \
	-v $(PWD)/tests:/app/tests \
	dvr-scan-file-organizer --input /videos --output /output

# Run linting inside a temporary container (no rebuild needed)
lint:
	docker run --rm -e PYTHONPATH=/app -v $(PWD)/dvr_scan_file_organizer:/app/dvr_scan_file_organizer \
	-v $(PWD)/tests:/app/tests --entrypoint pylint dvr-scan-file-organizer dvr_scan_file_organizer tests

# New formatting command
format:
	docker run --rm -v $(PWD)/dvr_scan_file_organizer:/app/dvr_scan_file_organizer \
	-v $(PWD)/tests:/app/tests --entrypoint black dvr-scan-file-organizer /app/dvr_scan_file_organizer /app/tests

# Combined quality check
quality: format lint

# Run tests inside a temporary container (no rebuild needed)
test:
	docker run --rm \
		-e PYTHONPATH=/app \
		-v $(PWD)/dvr_scan_file_organizer:/app/dvr_scan_file_organizer \
		-v $(PWD)/tests:/app/tests \
		--entrypoint pytest dvr-scan-file-organizer /app/tests

# Cleanup old Docker images
clean:
	docker rmi -f dvr-scan-file-organizer || true
	docker builder prune -f --filter "label=project=dvr-scan-file-organizer"
