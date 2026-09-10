"""Unit tests for processor module."""

from unittest.mock import patch

import pytest

from dvr_scan_file_organizer.processor import (
    SUPPORTED_EXTENSIONS,
    _build_dvr_scan_cmd,
    scan_videos,
)


def test_build_dvr_scan_cmd_without_config():
    """Config flag omitted when no config path."""
    cmd = _build_dvr_scan_cmd("/in.mp4", "/out.avi")
    assert cmd == ["dvr-scan", "-i", "/in.mp4", "-o", "/out.avi"]


def test_build_dvr_scan_cmd_with_config():
    """Config flag passed when config path set."""
    cmd = _build_dvr_scan_cmd("/in.mp4", "/out.avi", "/cfg/dvr-scan.cfg")
    assert cmd == [
        "dvr-scan",
        "-c",
        "/cfg/dvr-scan.cfg",
        "-i",
        "/in.mp4",
        "-o",
        "/out.avi",
    ]


def test_scan_videos_missing_input_dir(tmp_path):
    """Missing input directory raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="Input directory does not exist"):
        scan_videos(str(tmp_path / "missing"), str(tmp_path / "output"))


def test_scan_videos_empty_input_dir(tmp_path):
    """Empty input directory raises ValueError."""
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    with pytest.raises(ValueError, match="No supported video files found"):
        scan_videos(str(input_dir), str(tmp_path / "output"))


def test_scan_videos_copies_original_and_organizes(tmp_path):
    """Successful scan copies original and organizes motion/ + original/."""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()

    video = input_dir / "test.mp4"
    video.write_bytes(b"fake-video")

    def fake_dvr_scan(cmd, check=True):  # pylint: disable=unused-argument
        output_index = cmd.index("-o") + 1
        motion_file = cmd[output_index]
        with open(motion_file, "wb") as handle:
            handle.write(b"motion")

    with patch("subprocess.run", side_effect=fake_dvr_scan):
        scan_videos(str(input_dir), str(output_dir))

    assert (output_dir / "motion" / "test.mp4_motion.avi").exists()
    assert (output_dir / "original" / "test.mp4").exists()
    assert video.read_bytes() == b"fake-video"


def test_scan_videos_passes_config_to_dvr_scan(tmp_path):
    """Config path forwarded to dvr-scan subprocess."""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    (input_dir / "clip.mp4").write_bytes(b"x")
    config_path = str(tmp_path / "dvr-scan.cfg")
    captured_cmds = []

    def fake_dvr_scan(cmd, check=True):  # pylint: disable=unused-argument
        captured_cmds.append(cmd)
        output_index = cmd.index("-o") + 1
        with open(cmd[output_index], "wb") as handle:
            handle.write(b"motion")

    with patch("subprocess.run", side_effect=fake_dvr_scan):
        scan_videos(str(input_dir), str(output_dir), config_path=config_path)

    assert captured_cmds[0][:4] == ["dvr-scan", "-c", config_path, "-i"]


def test_supported_extensions_tuple():
    """Supported extensions match organizer expectations."""
    assert ".mp4" in SUPPORTED_EXTENSIONS
    assert ".avi" in SUPPORTED_EXTENSIONS
    assert ".mkv" in SUPPORTED_EXTENSIONS
