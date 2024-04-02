# Path: src/config.py
# Author: Jangsoo Park, Jiwoon Lee
# Last Modified: 2024-04-02
# Description: This script includes the configuration for the comparison of the submission images with the reference images.
# License: MIT License
#
# Disclaimer
# This program is provided as is without any guarantees or warranty. In no event shall the authors be liable for any damages or losses arising from the use of this program.
# This program does not guarantee the correctness of the comparison results. Please check the results manually.

import argparse
import warnings

shape_threshold = 5
error_threshold = 0.01
warnings.filterwarnings("ignore")

def get_config():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input-dir', dest='input_dir', type=str, default='submission', help='Directory containing submissions')
    parser.add_argument('--reference-dir', dest='reference_dir', type=str, default='reference', help='Directory containing reference images')
    parser.add_argument('--output-dir', dest='output_dir', type=str, default='out', help='Directory to save the result')
    parser.add_argument('--check_filetype', dest='check_filetype', type=str, default='pdf,cpp', help='Filetype to check')
    parser.add_argument('--p', dest='p', type=int, default=16, help='Number of processes')
    parser.add_argument('--shape-threshold', dest='shape_threshold', type=int, default=5, help='Threshold for shape comparison')
    parser.add_argument('--error-threshold', dest='error_threshold', type=float, default=0.01, help='Threshold for error comparison')
    return parser.parse_args()
