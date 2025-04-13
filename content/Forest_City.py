import numpy as np
from scipy.ndimage import gaussian_filter, distance_transform_edt
import matplotlib.pyplot as plt
from Forest import generate_clumpy_forest
from Forest import TREE

def generate_large_cluster_city_matrix(size, forest_matrix, smoothness=10.0, distance_influence=2.0, center_bias=2.0):
    """
    Generates a city layout matrix with population density favorably distributed:
    - -1 = TREE (unbuildable)
    - 0  = buildable but unpopulated
    - 1–8 = increasing levels of population density
    """
    # Step 1: Random noise, smoothed
    raw_noise = np.random.rand(size, size)
    smoothed = gaussian_filter(raw_noise, sigma=smoothness)

    # Step 2: Distance from trees
    tree_mask = (forest_matrix == TREE)
    distance_map = distance_transform_edt(~tree_mask)

    # Step 3: Distance from center (bias toward center)
    y, x = np.indices((size, size))
    center_y, center_x = size // 2, size // 2
    dist_to_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    center_bias_map = 1 - (dist_to_center / dist_to_center.max())  # 1 at center, 0 at corners

    # Step 4: Normalize input maps
    smoothed_norm = (smoothed - smoothed.min()) / (smoothed.max() - smoothed.min())
    distance_norm = (distance_map - distance_map.min()) / (distance_map.max() - distance_map.min())

    # Step 5: Combine factors
    biased_density = smoothed_norm * (distance_norm ** distance_influence) * (center_bias_map ** center_bias)

    # Step 6: Scale to 1–8, threshold very low values to 0 (no pop), and set trees to -1
    scaled_density = (biased_density / biased_density.max()) * 8
    city_matrix = scaled_density.astype(int)
    city_matrix[city_matrix < 1] = 0         # No population
    city_matrix[tree_mask] = -1              # Forest cells

    return city_matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(cell) for cell in row))

# Example usage
if __name__ == "__main__":
    size = 250
    smoothness = 50.0
    distance_influence = 0.05  # Tune this between 1.0 (mild) and 3.0 (strong effect)
    center_bias = 1.3  # center preference
    forest = generate_clumpy_forest(size, clump_scale=30.0)
    city = generate_large_cluster_city_matrix(size, forest, smoothness, distance_influence, center_bias)

    # Optional: visualize both matrices
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(forest, cmap="Greens", interpolation="nearest")
    plt.title("Original Forest Matrix")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(city, cmap="hot", interpolation="nearest")
    plt.title("City Population Density Matrix")
    plt.colorbar(label="Population Density")
    plt.axis('off')

    plt.tight_layout()
    plt.show()