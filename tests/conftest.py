"""Shared pytest fixtures."""

import shutil
import subprocess

import pytest


@pytest.fixture
def sample_video(tmp_path):
    """Generate a minimal MP4 test clip with ffmpeg."""
    if not shutil.which("ffmpeg"):
        pytest.skip("FFmpeg is required to generate test video")

    video_path = tmp_path / "test.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "testsrc=duration=1:size=320x240:rate=1",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(video_path),
        ],
        check=True,
        capture_output=True,
    )
    return video_path
