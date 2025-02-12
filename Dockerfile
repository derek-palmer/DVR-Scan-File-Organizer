# Dockerfile - Optimized for Live Mounting

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install required system packages (OpenGL, FFmpeg, dependencies)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies only
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Set entry point to run the processor module
ENTRYPOINT ["python", "-m", "dvrscan_organizer.processor"]
