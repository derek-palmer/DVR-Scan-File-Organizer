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
	docker build -t dvrscan-organizer .

# Run the container (mounts source code live)
run:
	docker run --rm -v $(PWD)/videos:/videos -v $(PWD)/output:/output \
	-v $(PWD)/dvrscan_organizer:/app/dvrscan_organizer \
	-v $(PWD)/tests:/app/tests dvrscan-organizer --input /videos --output /output

# Run linting inside a temporary container (no rebuild needed)
lint:
	docker run --rm -e PYTHONPATH=/app -v $(PWD)/dvrscan_organizer:/app/dvrscan_organizer \
	-v $(PWD)/tests:/app/tests --entrypoint pylint dvrscan-organizer dvrscan_organizer tests

# New formatting command
format:
	docker run --rm -v $(PWD)/dvrscan_organizer:/app/dvrscan_organizer \
	-v $(PWD)/tests:/app/tests --entrypoint black dvrscan-organizer /app/dvrscan_organizer /app/tests

# Combined quality check
quality: format lint

# Run tests inside a temporary container (no rebuild needed)
test:
	docker run --rm \
		-e PYTHONPATH=/app \
		-v $(PWD)/dvrscan_organizer:/app/dvrscan_organizer \
		-v $(PWD)/tests:/app/tests \
		--entrypoint pytest dvrscan-organizer tests

# Cleanup old Docker images
clean:
	docker rmi -f dvrscan-organizer || true
	docker system prune -f
