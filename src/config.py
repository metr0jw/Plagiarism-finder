import argparse

shape_threshold = 5
error_threshold = 0.01

def get_config():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input-dir', dest='input_dir', type=str, default='submission', help='Directory containing submissions')
    parser.add_argument('--reference-dir', dest='reference_dir', type=str, default='reference', help='Directory containing reference images')
    parser.add_argument('--output-dir', dest='output_dir', type=str, default='out', help='Directory to save the result')
    parser.add_argument('--check_filetype', dest='check_filetype', type=str, default='pdf,cpp', help='Filetype to check')
    parser.add_argument('--p', dest='p', type=int, default=1, help='Number of processes')
    parser.add_argument('--shape-threshold', dest='shape_threshold', type=int, default=5, help='Threshold for shape comparison')
    parser.add_argument('--error-threshold', dest='error_threshold', type=float, default=0.01, help='Threshold for error comparison')
    return parser.parse_args()
