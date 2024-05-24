from scipy.stats import norm
import numpy as np
from skimage import img_as_ubyte
from skimage.exposure import cumulative_distribution

def equalize_histogram(image, method):
    """Equalize the histogram of an image according to the provided method."""

    freq, bins = cumulative_distribution(image)
    target_bins = np.arange(255)

    if method == 'gaussian':
        gaussian = norm(128, 64)
        target_freq = gaussian.cdf(np.arange(255))

    elif method == 'linear':
        target_freq = np.linspace(0, 1, len(target_bins))

    elif method == 'exponential':
        # Define the exponential distribution
        beta = 50 # Exponential distribution parameter
        target_freq = 1 - np.exp(-np.arange(255)/beta)
    
    else:
        raise ValueError(f"Method '{method}' not implemented.")

    # Interpolate image with target distribution
    equalized_image = np.interp(image.flatten(), bins, freq)
    equalized_image = np.interp(equalized_image, target_freq, target_bins)
    
    return equalized_image.reshape(image.shape)

def equalize_rgb(image, method):
    """Equalize the histogram of an RGB image according to the provided method."""

    equalized_image = np.zeros_like(image)

    for channel in range(3):
        equalized_image[:, :, channel] = equalize_histogram(image[:, :, channel], method)

    return img_as_ubyte(equalized_image)
# image = equalize_histogram("t.png", method="gaussian")
# equalize_rgb(image, method='gaussian')