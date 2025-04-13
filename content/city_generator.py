import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

def generate_large_cluster_city_matrix(size, smoothness=4.0):
    """
    Generates a city layout matrix with larger and more distinct clusters of high and low density areas.
    - `smoothness`: Controls the spread of the density regions. Higher values result in larger clusters.
    """
    # Generate random noise matrix
    raw_noise = np.random.rand(size, size)  # values between 0 and 1
    
    # Apply a Gaussian filter with a larger sigma to create larger clusters
    smoothed = gaussian_filter(raw_noise, sigma=smoothness)
    
    # Normalize the values to be between 0 and 1
    normalized = (smoothed - smoothed.min()) / (smoothed.max() - smoothed.min())  # scale to 0-1
    
    # Scale the values to the desired range (0–8 for density)
    city_matrix = (normalized * 8).astype(int)
    
    return city_matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(cell) for cell in row))

# Example usage
if __name__ == "__main__":
    size = int(input("Enter city matrix size (e.g., 500): "))  # Use larger sizes for realism
    city = generate_large_cluster_city_matrix(size, smoothness=50.0)  # Increase smoothness for larger clusters
    
    print("\nCity Density Matrix:")
    print_matrix(city)
    
    # Optional: visualize the layout
    plt.imshow(city, cmap="hot", interpolation="nearest")
    plt.title("City Density Heatmap")
    plt.colorbar(label="Density")
    plt.show()