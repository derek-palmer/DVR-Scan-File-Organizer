# Dockerfile - Optimized for Live Mounting

FROM python:3.14-slim AS builder

WORKDIR /app

# Compiler toolchain for native wheels in the builder stage only.
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.14-slim

WORKDIR /app

# Runtime libs for dvr-scan[opencv-headless] + ffmpeg. No libgl1-mesa-glx:
# that package is gone on Debian trixie, and GL was only required for the
# removed non-headless opencv-python pin (#16).
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local

ENTRYPOINT ["python", "-m", "dvr_scan_file_organizer.processor"]

LABEL project="dvr-scan-file-organizer"
