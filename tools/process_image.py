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

from src.common import Student, Reference

def compare_image_wrapper(args):
    return compare_image(*args)

def compare_image_wrapper_ref(args):
    return compare_image(*args, reference=True)

def compare_image(submission_dir_a: str, submission_dir_b: str, reference: bool = False):
    '''
    Compare two images from two different directories.
    Args:
        submission_dir_a: Directory of the first student's image
        submission_dir_b: Directory of the second student's image
    '''
    # Check if the directories are the same
    if not reference and (submission_dir_a == submission_dir_b):
        return
    
    # Load image and reference image
    student_id_a = os.path.basename(submission_dir_a)
    student_id_b = os.path.basename(submission_dir_b)

    # Load list of images
    images_a = os.listdir(submission_dir_a)
    images_b = os.listdir(submission_dir_b)

    # Return if the number of images is 0
    if len(images_a) == 0 or len(images_b) == 0:
        return

    # Compare each image
    mse_values = []
    ssim_values = []
    psnr_values = []

    mse_min = 1e9
    mse_max = 0
    mse_avg = 0

    ssim_min = 1e9
    ssim_max = 0
    ssim_avg = 0

    psnr_min = 1e9
    psnr_max = 0
    psnr_avg = 0

    # TODO: Check rotation, flip, other loss, etc.
    for img_name_a in images_a:
        for img_name_b in images_b:
            # Load paths
            image_path_a = os.path.join(submission_dir_a, img_name_a)
            image_path_b = os.path.join(submission_dir_b, img_name_b)

            # Load the images
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
            mse = np.mean((image_a - image_b) ** 2)
            ssim_value = ssim(image_a, image_b, multichannel=True, win_size=11, channel_axis=2)
            psnr_value = psnr(image_a, image_b)

            mse_min = min(mse_min, mse)
            mse_max = max(mse_max, mse)
            mse_avg += mse

            ssim_min = min(ssim_min, ssim_value)
            ssim_max = max(ssim_max, ssim_value)
            ssim_avg += ssim_value

            psnr_min = min(psnr_min, psnr_value)
            psnr_max = max(psnr_max, psnr_value)
            psnr_avg += psnr_value
    
    mse_avg /= len(images_a) * len(images_b)
    ssim_avg /= len(images_a) * len(images_b)
    psnr_avg /= len(images_a) * len(images_b)

    mse_values.append((mse_min, mse_max, mse_avg))
    ssim_values.append((ssim_min, ssim_max, ssim_avg))
    psnr_values.append((psnr_min, psnr_max, psnr_avg))

    return student_id_a, student_id_b, mse_values, ssim_values, psnr_values

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

    if transparent_ratio > 0.95:
        return True
    
    # Check the ratio of white pixels
    white = 0
    for pixel in data:
        if pixel[:3] == (255, 255, 255):
            white += 1
    white_ratio = white / len(data)

    if white_ratio > 0.95:
        return True
    
    # Check the ratio of black pixels
    black = 0
    for pixel in data:
        if pixel[:3] == (0, 0, 0):
            black += 1
    black_ratio = black / len(data)

    if black_ratio > 0.95:
        return True
    
    # Check if the image is smaller than 11x11
    if image.size[0] < 11 or image.size[1] < 11:
        return True
    
    return False
