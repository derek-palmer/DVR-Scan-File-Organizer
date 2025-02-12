# DVR-Scan-Organizer

## Overview
DVR-Scan-Organizer is a Dockerized extension for DVR-Scan, designed to process multiple video files and organize output in a structured format.

This project:
- Supports batch video processing.
- Uses Docker for an isolated, reproducible environment.
- Includes automated linting and testing.

## Getting Started
### Prerequisites
- Install Docker: [Get Docker](https://docs.docker.com/get-docker/)

### Setup and Build
Clone the repository:
```sh
git clone https://github.com/derek-palmer/DVR-Scan-Organizer.git
cd DVR-Scan-Organizer
```

Build the Docker container:
```sh
make build
```

### Running DVR-Scan-Organizer
Ensure input videos are inside `videos/` and run:
```sh
make run
```
This mounts the `videos/` directory and processes all valid video files.

Output will be stored in `output/`.

## Development Workflow
### Run Linting
```sh
make lint
```
Runs inside a temporary Docker container without requiring a rebuild.

### Run Tests
```sh
make test
```
Tests run against the latest live-mounted code.

## Project Structure
```
DVR-Scan-Organizer/
│── dvrscan_organizer/      # Core processing logic
│── tests/                  # Unit tests
│── videos/                 # Input video files (mounted at runtime)
│── output/                 # Processed output files (mounted at runtime)
│── Dockerfile              # Container configuration
│── Makefile                # Automation for build/test/lint/run
│── requirements.txt        # Python dependencies
│── README.md               # Documentation
```

## Summary
- Dockerized for consistent behavior.
- Live-mounted volumes to avoid unnecessary rebuilds.
- Automated linting and testing inside Docker.
