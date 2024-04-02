# Path: tools/compare/text.py
# Author: Jiwoon Lee
# Last Modified: 2024-04-02
# Description: This script parses the text files in the specified directory and compares the submission texts with the reference texts.
# License: MIT License
#
# Disclaimer
# This program is provided as is without any guarantees or warranty. In no event shall the authors be liable for any damages or losses arising from the use of this program.
# This program does not guarantee the correctness of the comparison results. Please check the results manually.


import os

def parse_filenames(dir_name: str, ext: str):
    filenames = []
    for root, dirs, files in os.walk(dir_name):
        if len(files) > 0:
            # Append only files with the specified extension
            filenames.extend([os.path.join(root, f) for f in files if f.endswith(ext)])
    return filenames
