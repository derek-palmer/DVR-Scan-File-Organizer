"""Processor module for scanning videos using DVR-Scan."""

import argparse
import os
import shutil
import subprocess
import sys

from dvr_scan_file_organizer.organizer import organize_output

SUPPORTED_EXTENSIONS = (".mp4", ".avi", ".mkv")


def _find_videos(input_dir):
    """Return video filenames in input_dir with supported extensions."""
    videos = []
    for entry in os.scandir(input_dir):
        if entry.is_file():
            _, ext = os.path.splitext(entry.name)
            if ext.lower() in SUPPORTED_EXTENSIONS:
                videos.append(entry.name)
    return videos


def _build_dvr_scan_cmd(input_file, output_file, config_path=None):
    """Build dvr-scan command with optional config file."""
    cmd = ["dvr-scan"]
    if config_path:
        cmd.extend(["-c", config_path])
    cmd.extend(["-i", input_file, "-o", output_file])
    return cmd


def scan_videos(input_dir, output_dir, config_path=None):
    """Scans all video files in a directory and organizes the output."""
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    # Check if input and output resolve to the same location
    if os.path.exists(output_dir) and os.path.samefile(input_dir, output_dir):
        raise ValueError("Input and output directories cannot be the same location")

    videos = _find_videos(input_dir)
    if not videos:
        raise ValueError(
            f"No supported video files found in {input_dir}. "
            f"Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in videos:
        input_file = os.path.join(input_dir, file)
        output_file = os.path.join(output_dir, f"{file}_motion.avi")

        cmd = _build_dvr_scan_cmd(input_file, output_file, config_path)
        subprocess.run(cmd, check=True)

        # Copy original into output root so organizer can route to original/
        # Skip if input and output directories are the same
        output_copy_path = os.path.join(output_dir, file)
        if not os.path.samefile(input_file, output_copy_path):
            shutil.copy2(input_file, output_copy_path)

    organize_output(output_dir)


def main():
    """Main function for command-line execution."""
    parser = argparse.ArgumentParser(description="Batch process videos with DVR-Scan")
    parser.add_argument(
        "--input", required=True, help="Directory containing video files"
    )
    parser.add_argument(
        "--output", required=True, help="Directory to save processed videos"
    )
    parser.add_argument(
        "--config",
        default=os.environ.get("DVR_SCAN_CONFIG"),
        help="Path to dvr-scan.cfg (default: env DVR_SCAN_CONFIG if set)",
    )
    args = parser.parse_args()

    try:
        scan_videos(args.input, args.output, config_path=args.config)
    except (FileNotFoundError, ValueError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(
            f"DVR-Scan command failed with return code {exc.returncode}: {exc.cmd}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
