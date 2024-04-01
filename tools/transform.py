from skimage import transform
from skimage import metrics
from skimage import color
from skimage import io

def rotate(image, angle):
    return transform.rotate(image, angle)

def resize(image, shape):
    return transform.resize(image, shape)
