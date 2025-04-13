import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

def generate_smooth_city_matrix(size, smoothness=1.5):
    """
    Generates a realistic city layout matrix where higher density areas are clustered.
    - `smoothness`: Higher values create more gradual transitions between regions.
    """
    raw_noise = np.random.rand(size, size)  # values between 0 and 1
    smoothed = gaussian_filter(raw_noise, sigma=smoothness)
    normalized = (smoothed - smoothed.min()) / (smoothed.max() - smoothed.min())  # scale to 0-1
    city_matrix = (normalized * 9).astype(int)  # scale to 0–9 integer
    return city_matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(cell) for cell in row))

# Example usage
if __name__ == "__main__":
    size = int(input("Enter city matrix size (e.g., 20): "))
    city = generate_smooth_city_matrix(size)
    
    print("\nCity Density Matrix:")
    print_matrix(city)
    
    # Optional: visualize the layout
    plt.imshow(city, cmap="hot", interpolation="nearest")
    plt.title("City Density Heatmap")
    plt.colorbar(label="Density")
    plt.show()
