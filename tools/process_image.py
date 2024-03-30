import os

from spire.pdf.common import *
from spire.pdf import *

from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage import io
import numpy as np

from tqdm import tqdm

def compare_imgage_submission(submission_dir_a: str, submission_dir_b: str):
    # Load image and reference image

    return mse, ssim_value, psnr_value

def compare_image_reference(submission_dir: str, reference_dir: list):
    # Load image and reference image


    return mse, ssim_value, psnr_value

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
