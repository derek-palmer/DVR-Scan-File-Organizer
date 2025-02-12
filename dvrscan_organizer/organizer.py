""" Organizer module for structuring output files. """

import os
import shutil

def organize_output(output_dir):
    """ Organizes processed videos into structured folders. """
    categories = ["motion", "original"]

    for category in categories:
        category_path = os.path.join(output_dir, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if file.endswith("_motion.avi"):
            shutil.move(file_path, os.path.join(output_dir, "motion", file))
        elif file.endswith((".mp4", ".avi", ".mkv")):
            shutil.move(file_path, os.path.join(output_dir, "original", file))
