import io
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fitz
from PIL import Image

import numpy as np
import pandas as pd

from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage import io as skio

from tqdm import tqdm

from src.common import Student, Reference, get_database

def compare_image_submission(submission_dir_a: str, submission_dir_b: str):
    '''
    Compare two images from two different directories.
    Args:
        submission_dir_a: Directory of the first student's image
        submission_dir_b: Directory of the second student's image
    '''
    # Check if the directories are the same
    if submission_dir_a == submission_dir_b:
        return
    
    global database
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

        image_a = skio.imread(image_path_a)
        image_b = skio.imread(image_path_b)

        # Zero pad if the images are different sizes
        if image_a.shape != image_b.shape:
            pad_x = max(image_a.shape[0], image_b.shape[0])
            pad_y = max(image_a.shape[1], image_b.shape[1])
            image_a = np.pad(image_a, ((0, pad_x - image_a.shape[0]), (0, pad_y - image_a.shape[1]), (0, 0)), mode='constant')
            image_b = np.pad(image_b, ((0, pad_x - image_b.shape[0]), (0, pad_y - image_b.shape[1]), (0, 0)), mode='constant')
        
        # Remove alpha channel if it exists
        if image_a.shape[2] == 4:
            image_a = image_a[:, :, :3]
        if image_b.shape[2] == 4:
            image_b = image_b[:, :, :3]

        # Compare the images
        mse_value += np.mean((image_a - image_b) ** 2)
        ssim_value += ssim(image_a, image_b, multichannel=True, win_size=11, channel_axis=2)
        psnr_value += psnr(image_a, image_b)

    mse_value /= len(images_a)
    ssim_value /= len(images_a)
    psnr_value /= len(images_a)

    # Add the connection to the database
    database = get_database()
    database.add_connection(student_id_a, student_id_b, mse_value, ssim_value, psnr_value)

def compare_image_reference(submission_dir: str, reference_dir: list):
    '''
    Compare an image from a student's directory with multiple reference images.
    Args:
        submission_dir: Directory of the student's image
        reference_dir: List of directories of reference images
    '''
    global database
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
        image_a = skio.imread(image_path)

        for ref_dir, ref_id in zip(reference_images, reference_ids):
            for ref_image in ref_dir:
                image_path_b = os.path.join(ref_dir, ref_image)
                image_b = skio.imread(image_path_b)

                # Zero pad if the images are different sizes
                if image_a.shape != image_b.shape:
                    pad_x = max(image_a.shape[0], image_b.shape[0])
                    pad_y = max(image_a.shape[1], image_b.shape[1])
                    image_a = np.pad(image_a, ((0, pad_x - image_a.shape[0]), (0, pad_y - image_a.shape[1]), (0, 0)), mode='constant')
                    image_b = np.pad(image_b, ((0, pad_x - image_b.shape[0]), (0, pad_y - image_b.shape[1]), (0, 0)), mode='constant')

                # Remove alpha channel if it exists
                if image_a.shape[2] == 4:
                    image_a = image_a[:, :, :3]
                if image_b.shape[2] == 4:
                    image_b = image_b[:, :, :3]

                # Compare the images
                mse_values[-1] += np.mean((image_a - image_b) ** 2)
                ssim_values[-1] += ssim(image_a, image_b, multichannel=True, win_size=11, channel_axis=2)
                psnr_values[-1] += psnr(image_a, image_b)

        mse_values[-1] /= len(reference_ids)
        ssim_values[-1] /= len(reference_ids)
        psnr_values[-1] /= len(reference_ids)

    # Add the connection to the database
    database = get_database()
    database.add_connection(student_id, reference_ids, mse_values, ssim_values, psnr_values)


def extract_image(doc_path: str, is_reference: bool = False):
    # Check if docx or pdf
    # If docx, convert to pdf
    # If pdf, extract images
    if doc_path.endswith('.docx'):
        # Convert docx to pdf
        doc = fitz.open()
        doc.insert_pdf(doc_path)
        pdf_path = doc_path.replace('.docx', '.pdf')
        doc.save(pdf_path)
        doc.close()
    else:
        pdf_path = doc_path

    # Extract images from the pdf
    images = []
    pdf = fitz.open(pdf_path)
    for page_num in range(pdf.page_count):
        page = pdf.load_page(page_num)
        image_list = page.get_images(full=True)
        for image in image_list:
            xref = image[0]
            base_image = pdf.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    pdf.close()

    # Extract the student ID from the doc_path
    student_id = os.path.basename(os.path.dirname(doc_path))

    if is_reference:
        buf = student_id
        student_id = 'ref_' + buf

    # Create the output directory for the student if it doesn't exist
    output_dir = f'./buffer/{student_id}'
    os.makedirs(output_dir, exist_ok=True)

    # Save the images
    for idx, image in enumerate(images):
        # Save if not dummy image
        if not is_dummy(image):
            image.save(os.path.join(output_dir, f'{idx}.png'))

    
def is_dummy(image: Image):
    # Input: PIL Image
    # Check if the image is a dummy image
    # All white, all black, mostly white, mostly black, mostly transparent (threshold 0.9)
    
    # Check the ratio of transparent pixels
    image = image.convert('RGBA')
    data = image.getdata()
    transparent = 0
    for pixel in data:
        if pixel[3] == 0:
            transparent += 1
    transparent_ratio = transparent / len(data)

    if transparent_ratio > 0.9:
        return True
    
    # Check the ratio of white pixels
    white = 0
    for pixel in data:
        if pixel[:3] == (255, 255, 255):
            white += 1
    white_ratio = white / len(data)

    if white_ratio > 0.9:
        return True
    
    # Check the ratio of black pixels
    black = 0
    for pixel in data:
        if pixel[:3] == (0, 0, 0):
            black += 1
    black_ratio = black / len(data)

    if black_ratio > 0.9:
        return True
    
    # Check if the image is smaller than 11x11
    if image.size[0] < 11 or image.size[1] < 11:
        return True
    
    return False
