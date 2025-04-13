import numpy as np
from pyqubo import Binary
from neal import SimulatedAnnealingSampler
from scipy.ndimage import zoom
import matplotlib.pyplot as plt
from Firethreat import predict_fire_threat

# Function to resize the danger map to a 50x50 format directly
def resize_heatmap(original_map, target_size=50):
    """Resizes and rescales the original danger map to target size using interpolation."""
    h, w = original_map.shape
    resized_map = zoom(original_map, (target_size / h, target_size / w), order=1)  # Bilinear interpolation

    # Normalize to 0–9 range
    min_val, max_val = resized_map.min(), resized_map.max()
    if max_val > min_val:
        resized_map = (resized_map - min_val) / (max_val - min_val) * 9
    else:
        resized_map = np.zeros_like(resized_map)

    return resized_map

# QUBO conversion function
def matrix_to_qubo(matrix, alpha=2, beta=4, allow_adjacent_penalty=True):
    n = matrix.shape[0]
    variables = {}

    for i in range(n):
        for j in range(n):
            variables[(i, j)] = Binary(f"x{i}{j}")

    # Objective: maximize matrix values (minimize negative weighted sum)
    H = -sum(matrix[i][j] * variables[(i, j)] for i in range(n) for j in range(n))

    # Penalty for number of units used
    total_selected = sum(variables[(i, j)] for i in range(n) for j in range(n))
    H += float(alpha).__float__() * total_selected

    # Penalty for adjacent units selected together
    if allow_adjacent_penalty:
        for i in range(n):
            for j in range(n):
                if i < n - 1:
                    H += float(beta).__float__() * variables[(i, j)] * variables[(i + 1, j)]
                if j < n - 1:
                    H += float(beta).__float__() * variables[(i, j)] * variables[(i, j + 1)]

    model = H.compile()
    qubo, offset = model.to_qubo()
    return qubo, offset, model

# Solving the QUBO with the Simulated Annealing Sampler
def solve_qubo_with_neal(matrix, alpha=2, beta=4, num_reads=100):
    qubo, offset, model = matrix_to_qubo(matrix, alpha=alpha, beta=beta)
    sampler = SimulatedAnnealingSampler()
    sampleset = sampler.sample_qubo(qubo, num_reads=num_reads)
    decoded_samples = model.decode_sampleset(sampleset)
    best_sample = decoded_samples[0]

    n = matrix.shape[0]
    solution_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            varname = f"x{i}{j}"
            solution_matrix[i, j] = best_sample.sample.get(varname, 0)

    return solution_matrix, best_sample.energy + offset

# Visualization function
def plot_all_heatmaps(original_map, resized_map, solution_map):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    im1 = axes[0].imshow(original_map, cmap="Blues", interpolation='nearest')
    axes[0].set_title("Original Threat Map (250x250)")
    fig.colorbar(im1, ax=axes[0])

    im2 = axes[1].imshow(resized_map, cmap="Blues", interpolation='nearest')
    axes[1].set_title("Resized Heatmap (50x50)")
    fig.colorbar(im2, ax=axes[1])

    im3 = axes[2].imshow(solution_map, cmap="Blues", interpolation='nearest')
    axes[2].set_title("Optimized Deployment Solution")
    fig.colorbar(im3, ax=axes[2])

    plt.tight_layout()
    plt.show()

# Main pipeline
def run_qubo_pipeline():
    # Get the full-size danger map
    danger_map, _, _, _ = predict_fire_threat()

    # Resize the original map directly to 50x50
    resized_map = resize_heatmap(danger_map)

    # Solve the QUBO problem
    solution, energy = solve_qubo_with_neal(resized_map, alpha=7, beta=4)

    # Visualize
    plot_all_heatmaps(danger_map, resized_map, solution)

    # Print results
    print("Optimal Response Deployment:\n", solution)
    print("Energy (QUBO Objective):", energy)
    print("Units used:", int(solution.sum()))

if __name__ == "__main__":
    run_qubo_pipeline()