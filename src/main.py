# Path: src/main.py
# Author: Jangsoo Park, Jiwoon Lee
# Last Modified: 2024-04-02
# Description: This script compares the submission images with the reference images and saves the result in the output directory.
# Usage: python main.py --input-dir <input_dir> --reference-dir <reference_dir> --output-dir <output_dir> --check_filetype <check_filetype>
# Example: python main.py --input-dir ./outputs --reference-dir ./reference --output-dir ./result --check_filetype pdf,cpp
# Arguments:
#   --input-dir: Directory containing submissions
#   --reference-dir: Directory containing reference images
#   --output-dir: Directory to save the result
#   --check_filetype: Filetype to check
# License: MIT License
# Notice
# This program compares predefined file types. If you want to compare other file types, please add the file type to supported_doc_types, supported_code_types, supported_etc_types in common.py.
#
# Disclaimer
# This program is provided as is without any guarantees or warranty. In no event shall the authors be liable for any damages or losses arising from the use of this program.
# This program does not guarantee the correctness of the comparison results. Please check the results manually.

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
from tools.compare.image import extract_image, compare_image, compare_image_wrapper, compare_image_wrapper_ref

args = config.get_config()
database = common.DB()

def parse_filenames(directory, check_doc_types, check_code_types, check_etc_types, database, is_reference=False):
    """
    Parse filenames in the directory and add them to the database.
    
    Args:
        directory (str): Directory path to scan for files
        check_doc_types (list): List of document file extensions to check
        check_code_types (list): List of code file extensions to check
        check_etc_types (list): List of other file extensions to check
        database (common.DB): Database to store the parsed files
        is_reference (bool): Whether parsing reference files or submissions
        
    Returns:
        int: Number of files parsed
    """
    file_count = 0
    
    for root, dirs, files in os.walk(directory):
        if len(files) > 0:
            file_count += len(files)
            # Path name as student_id or reference_id
            entity_id = os.path.basename(root)
            
            if is_reference:
                entity = common.Reference()
            else:
                entity = common.Student()
                
            entity.set_id(entity_id)
            
            for f in files:
                if f.endswith(tuple(check_doc_types)):
                    entity.add_doc_dir(os.path.join(root, f))
                elif f.endswith(tuple(check_code_types)):
                    entity.add_code_dir(os.path.join(root, f))
                elif f.endswith(tuple(check_etc_types)):
                    entity.add_etc_dir(os.path.join(root, f))
                    
            if is_reference:
                database.add_reference(entity)
            else:
                database.add_student(entity)
                
    return file_count

def compare_files(database, check_doc_types, check_code_types, check_etc_types, args):
    """
    Compare files based on their types and save results.
    
    Args:
        database (common.DB): Database containing files to compare
        check_doc_types (list): List of document file extensions to check
        check_code_types (list): List of code file extensions to check
        check_etc_types (list): List of other file extensions to check
        args: Command line arguments
        
    Returns:
        None
    """
    # If check document
    if len(check_doc_types) > 0:
        # Get student and reference directories
        sub_doc_names, ref_doc_names = database.get_documents()
        
        ### Extract images from document files ###
        print('Checking document files...')
        print('Extracting images...')
        if args.p > 1:
            parmap.map(extract_image, sub_doc_names, pm_pbar=True, pm_processes=args.p)
            parmap.map(extract_image, ref_doc_names, pm_pbar=True, pm_processes=args.p, is_reference=True)
        else:
            for s in tqdm(sub_doc_names, desc='Extracting images... (Submission)'):
                extract_image(s)
            for r in tqdm(ref_doc_names, desc='Extracting images... (Reference)'):
                extract_image(r, is_reference=True)
                
        # Get directories in buffer
        sub_image_dirs = glob.glob(os.path.join(common.buffer_dir, '*'))
        ref_image_dirs = glob.glob(os.path.join(common.buffer_dir, 'ref_*'))

        # Remove ref_image_dirs from sub_image_dirs
        sub_image_dirs = [s for s in sub_image_dirs if s not in ref_image_dirs]
        print(f'Finished extracting images')
        
        ### Compare images ###
        print('Comparing images... (Submission and Submission)')

        if args.p > 1:
            compare_args = [(s0, s1) for i, s0 in enumerate(sub_image_dirs) for s1 in sub_image_dirs[i+1:]]
            compare_result = parmap.map(compare_image_wrapper, compare_args, pm_pbar=True, pm_processes=args.p)
        else:
            compare_result = []
            for i, s0 in enumerate(tqdm(sub_image_dirs, desc='Comparing images... (Submission and Submission)')):
                for s1 in sub_image_dirs[i+1:]:
                    compare_result.append(compare_image(s0, s1))
        
        # Connect to database
        for result in compare_result:
            if result is not None:
                database.add_connection(*result)

        print('Comparing images... (Submission and Reference)')
        if args.p > 1:
            compare_args = [(s, r) for s in sub_image_dirs for r in ref_image_dirs]
            compare_result = parmap.map(compare_image_wrapper, compare_args, pm_pbar=True, pm_processes=args.p)
        else:
            compare_result = []
            for s in tqdm(sub_image_dirs, desc='Comparing images... (Submission and Reference)'):
                for r in ref_image_dirs:
                    compare_result.append(compare_image(s, r, reference=True))

        # Connect to database
        for result in compare_result:
            if result is not None:
                database.add_connection(*result, reference=True)

        # Save the result using pandas
        buf = [[key, *value] for key, values in database.connections.items() for value in values]
        # Unpack ssim, psnr, mse
        buf = [[*b[:2], *b[2][0], *b[3][0], *b[4][0]] for b in buf]
        df = pd.DataFrame(buf, columns=['student_id_a', 'student_id_b',
                                        'mse_min', 'mse_max', 'mse_avg',
                                        'ssim_min', 'ssim_max', 'ssim_avg',
                                        'psnr_min', 'psnr_max', 'psnr_avg'])
        df.to_csv(os.path.join(args.output_dir, 'result.csv'), index=False)
            
        ### Compare texts in document files ###

    # If check code
    if len(check_code_types) > 0:
        print('Checking code files...')
        code_result = []
    
    # If check etc
    if len(check_etc_types) > 0:
        print('Checking etc files...')
        etc_result = []

def main():
    # Parse check_filetype into a list
    check_filetype = args.check_filetype.split(',')

    # Check supported file types
    assert len(check_filetype) > 0, 'check_filetype must be specified'
    assert check_filetype not in common.supported_types, f'Supported file types are {common.supported_types}. \
        Check github.com/metr0jw/Plagiarism-finder to ask for support \
        or add the file type to supported_doc_types, supported_code_types, supported_etc_types in src/common.py.'

    # Select supported file types, ex) ['docx', 'pdf', 'c', 'cpp', 'h', 'hpp', 'py', 'java', ...]
    check_doc_types = [t for t in check_filetype if t in common.supported_doc_types]     # ['docx', 'pdf']
    check_code_types = [t for t in check_filetype if t in common.supported_code_types]   # ['c', 'cpp', ...]
    check_etc_types = [t for t in check_filetype if t in common.supported_etc_types]     # ['txt', 'csv', ...]

    # Set threshold values
    shape_threshold = args.shape_threshold
    error_threshold = args.error_threshold
    os.makedirs(args.output_dir, exist_ok=True)

    # Parse filenames and add to database
    submission_count = parse_filenames(args.input_dir, check_doc_types, check_code_types, check_etc_types, database)
    reference_count = parse_filenames(args.reference_dir, check_doc_types, check_code_types, check_etc_types, database, is_reference=True)

    # Print information
    print(f'Num submissions: {submission_count}')
    print(f'References: {reference_count}')
    print(f'Filetype to check: {check_filetype}')
    print(f'I/O Directories: {args.input_dir}, {args.reference_dir}, {args.output_dir}')
    print(f'Error Threshold: {error_threshold}')
    print(f'Shape Threshold: {shape_threshold}')

    # Compare files
    compare_files(database, check_doc_types, check_code_types, check_etc_types, args)


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