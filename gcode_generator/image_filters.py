import numpy as np
from skimage import feature
from skimage import filters
from skimage.filters.thresholding import _cross_entropy
from skimage.filters import threshold_otsu, rank
from skimage.morphology import disk

def extract_contours(arr, sigma=1.5):
    # filtered = feature.canny(arr, sigma=sigma)
    filtered = filters.sobel(arr)
    return filtered

def binarize(arr):
    print(arr)
    print("min = ", np.min(arr))
    print("max = ", np.max(arr))
    arr = (arr * 255).astype(np.uint8)

    # thresholds = np.arange(np.min(arr) + 1.5, np.max(arr) - 1.5)
    # entropies = [_cross_entropy(arr, t) for t in thresholds]
    # optimal_threshold = thresholds[np.argmin(entropies)]

    t_otsu = threshold_otsu(arr)
    return arr > t_otsu

def binarize_local(arr):
    arr = (arr * 255).astype(np.uint8)
    radius = 15
    selem = disk(radius)

    local_otsu = rank.otsu(arr, selem)
    return local_otsu