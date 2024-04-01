# Deprecated: This script is deprecated. Please use the script in tools/compare_images.py
# MSE, SSIM, PSNR
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage import io
from tqdm import tqdm

def compare_image(image_path, reference_path):
    # Load image and reference image
    image = io.imread(image_path)
    reference = io.imread(reference_path)

    # Compare the images
    mse = np.mean((image - reference) ** 2)
    ssim_value = ssim(image, reference, multichannel=True)
    psnr_value = psnr(image, reference)

    return mse, ssim_value, psnr_value