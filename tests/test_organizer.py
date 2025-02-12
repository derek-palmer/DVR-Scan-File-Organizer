""" Unit tests for organizer module. """

from dvrscan_organizer.organizer import organize_output


def test_organize_output(tmp_path):
    """Tests the organize_output function."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    (output_dir / "test_motion.avi").touch()
    (output_dir / "test.mp4").touch()

    organize_output(str(output_dir))

    assert (output_dir / "motion" / "test_motion.avi").exists()
    assert (output_dir / "original" / "test.mp4").exists()


if __name__ == "__main__":
    print("Test organizer module loaded successfully.")
