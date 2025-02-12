""" Unit tests for processor module. """

import os
import shutil
from pathlib import Path
import subprocess
import pytest
from dvrscan_organizer.processor import scan_videos

@pytest.mark.skipif(
    not shutil.which("ffmpeg"), reason="FFmpeg is required for DVR-Scan"
)
def test_scan_videos(tmp_path):
    """ Tests the scan_videos function with a valid video file. """
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    sample_video = Path("/app/tests/assets/sample.mp4")
    if not sample_video.exists():
        pytest.skip("Skipping test: sample video not found")

    shutil.copy(sample_video, input_dir / "test.mp4")

    try:
        scan_videos(str(input_dir), str(output_dir))
    except FileNotFoundError as e:
        pytest.fail(f"scan_videos raised a FileNotFoundError: {e}")
    except OSError as e:
        pytest.fail(f"scan_videos raised an OSError: {e}")
    except (RuntimeError, subprocess.CalledProcessError) as e:
        pytest.fail(f"scan_videos raised an unexpected exception: {e}")

    assert len(os.listdir(output_dir)) > 0

if __name__ == "__main__":
    print("Test processor module loaded successfully.")
