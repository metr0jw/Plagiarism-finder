import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spire.pdf.common import *
from spire.pdf import *

import numpy as np
import pandas as pd

from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage import io

from tqdm import tqdm

from src.common import Student, Reference

def compare_image_submission(submission_dir_a: str, submission_dir_b: str):
    '''
    Compare two images from two different directories.
    Args:
        submission_dir_a: Directory of the first student's image
        submission_dir_b: Directory of the second student's image
    '''
    # Load image and reference image
    student_id_a = os.path.basename(submission_dir_a)
    student_id_b = os.path.basename(submission_dir_b)

    # Load list of images
    images_a = os.listdir(submission_dir_a)
    images_b = os.listdir(submission_dir_b)

    # Compare each image
    mse_value = 0
    ssim_value = 0
    psnr_value = 0

    # TODO: Check rotation, flip, other loss, etc.
    for image_a, image_b in zip(images_a, images_b):
        image_path_a = os.path.join(submission_dir_a, image_a)
        image_path_b = os.path.join(submission_dir_b, image_b)

        image_a = io.imread(image_path_a)
        image_b = io.imread(image_path_b)

        # Compare the images
        mse_value += np.mean((image_a - image_b) ** 2)
        ssim_value += ssim(image_a, image_b, multichannel=True)
        psnr_value += psnr(image_a, image_b)

    mse_value /= len(images_a)
    ssim_value /= len(images_a)
    psnr_value /= len(images_a)

    return mse_value, ssim_value, psnr_value, student_id_a, student_id_b

def compare_image_reference(submission_dir: str, reference_dir: list):
    '''
    Compare an image from a student's directory with multiple reference images.
    Args:
        submission_dir: Directory of the student's image
        reference_dir: List of directories of reference images
    '''
    # Load image and reference image
    student_id = os.path.basename(submission_dir)
    reference_ids = [os.path.basename(ref) for ref in reference_dir]

    # Load list of images
    images = os.listdir(submission_dir)
    reference_images = [os.listdir(ref) for ref in reference_dir]

    # Compare each image
    mse_values = []
    ssim_values = []
    psnr_values = []

    # TODO: Check rotation, flip, other loss, etc.
    for image in images:
        image_path = os.path.join(submission_dir, image)
        image_a = io.imread(image_path)

        mse_values.append(0)
        ssim_values.append(0)
        psnr_values.append(0)

        for ref_dir, ref_id in zip(reference_images, reference_ids):
            for ref_image in ref_dir:
                image_path_b = os.path.join(ref_dir, ref_image)
                image_b = io.imread(image_path_b)

                # Compare the images
                mse_values[-1] += np.mean((image_a - image_b) ** 2)
                ssim_values[-1] += ssim(image_a, image_b, multichannel=True)
                psnr_values[-1] += psnr(image_a, image_b)

        mse_values[-1] /= len(reference_ids)
        ssim_values[-1] /= len(reference_ids)
        psnr_values[-1] /= len(reference_ids)

    return mse_values, ssim_values, psnr_values, student_id, reference_ids


def extract_image(doc_path: str, is_reference: bool = False):
    # Create a PdfDocument object
    doc = PdfDocument()

    # Check if doc is a PDF or DOCX file
    # If it is a PDF file, load the file, otherwise, convert the DOCX file to a PDF file and load it
    if doc_path.endswith('.pdf'):
        doc.LoadFromFile(doc_path)
    else:  # docx
        doc.LoadFromStream(doc_path)

    # Extract the student ID from the doc_path
    student_id = os.path.basename(os.path.dirname(doc_path))

    if is_reference:
        buf = student_id
        student_id = 'ref_' + buf
    
    # Create the output directory for the student if it doesn't exist
    output_dir = f'./buffer/{student_id}'
    os.makedirs(output_dir, exist_ok=True)

    # Extract images from the page
    images = []
    for i in range(doc.Pages.Count):
        page = doc.Pages.get_Item(i)
        for image in page.ExtractImages():
            images.append(image)

    # Save images to the specified location with the specified format extension
    for index, image in enumerate(images, start=1):
        image_file_name = f'{output_dir}/image_{index}.png'
        image.Save(image_file_name, ImageFormat.get_Png())

    doc.Close()
