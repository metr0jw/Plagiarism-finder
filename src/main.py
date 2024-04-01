# Author: Jangsoo Park, Jiwoon Lee
# Last Modified: 2024-04-01
# Description: This script compares the submission images with the reference images and saves the result in the output directory.
# Usage: python main.py --input-dir <input_dir> --reference-dir <reference_dir> --output-dir <output_dir> --check_filetype <check_filetype>
# Example: python main.py --input-dir ./outputs --reference-dir ./reference --output-dir ./result --check_filetype pdf,cpp
# Arguments:
#   --input-dir: Directory containing submissions
#   --reference-dir: Directory containing reference images
#   --output-dir: Directory to save the result
#   --check_filetype: Filetype to check
# License: MIT License

import numpy as np
import pandas as pd

from multiprocessing import Pool
from functools import partial
from parmap import parmap
from tqdm import tqdm

import glob
import sys
import os
# add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import common
import config
from tools.process_image import extract_image, compare_image_submission, compare_image_reference

args = config.get_config()

def main():
    # Parse check_filetype into a list
    check_filetype = args.check_filetype.split(',')

    # Check supported file types
    assert len(check_filetype) > 0, 'check_filetype must be specified'
    assert check_filetype not in common.supported_types, f'Supported file types are {common.supported_types}. \
        Ask to Jangsoo Park(@jangsoopark), Jiwoon Lee(@metr0jw)'

    # Select supported file types, ex) ['docx', 'pdf', 'c', 'cpp', 'h', 'hpp', 'py', 'java', ...]
    check_doc_types = [t for t in check_filetype if t in common.supported_doc_types]     # ['docx', 'pdf']
    check_code_types = [t for t in check_filetype if t in common.supported_code_types]   # ['c', 'cpp', ...]
    check_etc_types = [t for t in check_filetype if t in common.supported_etc_types]     # ['txt', 'csv', ...]

    # Set threshold values
    shape_threshold = args.shape_threshold
    error_threshold = args.error_threshold
    os.makedirs(args.output_dir, exist_ok=True)

    database = common.DB()  # Initialize database
    submission_count = 0    # Initialize submission count
    reference_count = 0     # Initialize reference count

    # TODO: functionize parse_filenames
    for root, dirs, files in os.walk(args.input_dir):
        if len(files) > 0:
            submission_count += len(files)
            # Path name as student_id
            student_id = os.path.basename(root)
            student = common.Student()
            student.set_id(student_id)
            for f in files:
                if f.endswith(tuple(check_doc_types)):
                    student.add_doc_dir(os.path.join(root, f))
                elif f.endswith(tuple(check_code_types)):
                    student.add_code_dir(os.path.join(root, f))
                elif f.endswith(tuple(check_etc_types)):
                    student.add_etc_dir(os.path.join(root, f))

            database.add_student(student)

    for root, dirs, files in os.walk(args.reference_dir):
        if len(files) > 0:
            reference_count += len(files)
            # Path name as student_id
            reference_id = os.path.basename(root)
            reference = common.Reference()
            reference.set_id(reference_id)
            for f in files:
                if f.endswith(tuple(check_doc_types)):
                    reference.add_doc_dir(os.path.join(root, f))
                elif f.endswith(tuple(check_code_types)):
                    reference.add_code_dir(os.path.join(root, f))
                elif f.endswith(tuple(check_etc_types)):
                    reference.add_etc_dir(os.path.join(root, f))

            database.add_reference(reference)
    # TODO_END

    # Print information
    print(f'Num submissions: {submission_count}')
    print(f'References: {reference_count}')
    print(f'Filetype to check: {check_filetype}')
    print(f'I/O Directories: {args.input_dir}, {args.reference_dir}, {args.output_dir}')
    print(f'Error Threshold: {error_threshold}')
    print(f'Shape Threshold: {shape_threshold}')

    # TODO: functionize compare_files
    # Execute
    # If check document
    if len(check_doc_types) > 0:
        print('Checking document files...')
        print('Extracting images...')
        if args.p > 1:
            parmap.map(extract_image, sub_doc_names, pm_pbar=True, pm_processes=args.p)
            parmap.map(extract_image, ref_doc_names, pm_pbar=True, pm_processes=args.p, is_reference=True)
        else:
            for s in sub_doc_names:
                extract_image(s)
            for r in ref_doc_names:
                extract_image(r, is_reference=True)
        
        # Get directoreis in buffer
        sub_image_dirs = glob.glob(os.path.join(common.buffer_dir, '*'))        # ['student_id1', 'student_id2', ...] in absolute path
        ref_image_dirs = glob.glob(os.path.join(common.buffer_dir, 'ref_*'))    # ['ref_student_id1', 'ref_student_id2', ...] in absolute path

        # Remove ref_image_dirs from sub_image_dirs
        sub_image_dirs = [s for s in sub_image_dirs if s not in ref_image_dirs]

        print(f'Num extracted images: {len(sub_image_dirs)}')
        print(f'Num reference images: {len(ref_image_dirs)}')
        print(f'Finished extracting images')
        
        # Compare images
        print('Comparing images... (Submission and Submission)')
        image_result_sub = []
        if args.p > 1:
            compare_image_partial = partial(compare_image_submission, ref_image_dirs=ref_image_dirs)
            image_result_sub = parmap.map(compare_image_partial, sub_image_dirs, pm_pbar=True, pm_processes=args.p)
        else:
            for s in sub_image_dirs:
                image_result_sub.append(compare_image_submission(s, ref_image_dirs))

        print('Comparing images... (Submission and Reference)')
        image_result_ref = []
        if args.p > 1:
            compare_image_partial = partial(compare_image_reference, ref_image_dirs=sub_image_dirs)
            image_result_ref = parmap.map(compare_image_partial, ref_image_dirs, pm_pbar=True, pm_processes=args.p)
        else:
            for r in ref_image_dirs:
                image_result_ref.append(compare_image_reference(r, sub_image_dirs))

    # If check code
    if len(check_code_types) > 0:
        print('Checking code files...')
        code_result = []
    
    # If check etc
    if len(check_etc_types) > 0:
        print('Checking etc files...')
        etc_result = []
        

'''
def main():
    shape_threshold = 5
    error_threshold = 0.01
    os.makedirs(args.output_dir, exist_ok=True)

    # Get reference DB images
    ref_image_names = []
    for root, dirs, files in os.walk(args.reference_dir):
        if len(files) > 0:
            # Append only png files
            ref_image_names.extend([os.path.join(root, f) for f in files if f.endswith('.png')])

    submissions = os.listdir(args.input_dir)

    print(f'Num reference images: {len(ref_image_names)}')
    print(f'Num submissions: {len(submissions)}')

    # Compare each submission with reference images
    for submission in submissions:
        image_list = glob.glob(os.path.join(args.input_dir, submission, '*/*.png'))

        for s in image_list:
            image = io.imread(s)
            ih, iw, _ = image.shape
            submission_report_name = os.path.basename(os.path.dirname(os.path.dirname(s)))
            if image.shape[-1] > 3:
                image = color.rgba2rgb(image)

            for r in tqdm(ref_image_names, desc=f'{submission_report_name} {os.path.basename(s)}'):
                reference = io.imread(r)

                if reference.shape[-1] > 3:
                    reference = color.rgba2rgb(reference)

                rh, rw, _ = reference.shape
                reference_report_name = os.path.basename(os.path.dirname(os.path.dirname(r)))
                if abs(ih - rh) > shape_threshold or abs(iw - rw) > shape_threshold:
                    continue

                h = min(ih, rh)
                w = min(iw, rw)

                image = transform.resize(image, (h, w), anti_aliasing=True)
                reference = transform.resize(reference, (h, w), anti_aliasing=True)
                ssim = metrics.structural_similarity(
                    color.rgb2gray(image),
                    color.rgb2gray(reference),
                    data_range=1)

                psnr = metrics.peak_signal_noise_ratio(image, reference, data_range=1)
                mse = metrics.mean_squared_error(image, reference)
                if mse < error_threshold:
                    f = open(os.path.join(args.output_dir, f'{submission_report_name}.txt'), mode='at', encoding='utf-8')
                    f.write('==============================================================\n')
                    f.write(f'Input Report: {submission_report_name}\n')
                    f.write(f'\tImage Name: {os.path.basename(s)}\n')
                    f.write(f'\tImage Path: {s}\n')
                    f.write(f'Reference Report: {reference_report_name}\n')
                    f.write(f'\tImage Name: {os.path.basename(r)}\n')
                    f.write(f'\tImage Path: {r}\n')
                    f.write(f'SSIM: {ssim}\n')
                    f.write(f'PSNR: {psnr}\n')
                    f.write(f'MSE: {mse}\n\n')
                    f.close()
'''


if __name__ == '__main__':
    sys.exit(main())
