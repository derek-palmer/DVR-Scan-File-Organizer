""" Processor module for scanning videos using DVR-Scan. """

import os
import argparse
import subprocess
from dvrscan_organizer.organizer import organize_output


def scan_videos(input_dir, output_dir):
    """Scans all video files in a directory and organizes the output."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir(input_dir):
        if file.endswith((".mp4", ".avi", ".mkv")):
            input_file = os.path.join(input_dir, file)
            output_file = os.path.join(output_dir, f"{file}_motion.avi")

            # Run DVR-Scan on each video file
            cmd = ["dvr-scan", "-i", input_file, "-o", output_file]
            subprocess.run(cmd, check=True)

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
    args = parser.parse_args()

    scan_videos(args.input, args.output)


if __name__ == "__main__":
    main()
