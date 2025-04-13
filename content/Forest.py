import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

EMPTY, TREE = 0, -1

def generate_clumpy_forest(size=250, clump_scale=35, tree_ratio=0.5, seed=None):
    if seed is not None:
        np.random.seed(seed)

    # Ensure clump_scale results in an integer low_res_size
    low_res_size = max(1, int(size // clump_scale))  # Force integer by casting to int

    # Generate very low-res noise to create large clumps
    noise = np.random.rand(low_res_size, low_res_size)

    # Bicubic upscaling to smooth the clumps
    smooth_noise = zoom(noise, size / low_res_size, order=3)
    smooth_noise = smooth_noise[:size, :size]

    # Threshold to split TREE vs EMPTY while maintaining tree_ratio
    threshold = np.percentile(smooth_noise, 100 * (1 - tree_ratio))

    # Create forest matrix using TREE = -1 and EMPTY = 0
    forest = np.full((size, size), EMPTY)
    forest[smooth_noise > threshold] = TREE

    return forest

if __name__ == "__main__":
    # Only run this if Forest.py is run directly, not when it's imported
    size = 250
    forest = generate_clumpy_forest(size, clump_scale=30.0)

    # Visualization (this won't run when imported in Forest_City.py)
    plt.imshow(forest, cmap="Greens", interpolation="nearest")
    plt.title("Generated Forest")
    plt.axis("off")
    plt.show()