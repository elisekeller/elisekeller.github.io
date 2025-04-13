import numpy as np
import matplotlib.pyplot as plt
from Forest import generate_clumpy_forest, TREE as TREE_MARKER
from Forest_City import generate_large_cluster_city_matrix
from Fire_simulation import FireGrid, FIRE, TREE
import time

def normalize(matrix):
    max_val = matrix.max()
    return matrix / max_val if max_val > 0 else matrix

def predict_fire_threat():
    random_seed = int(time.time())
    np.random.seed(random_seed)

    try:
        user_steps = int(input("Enter number of initial fire steps: "))
    except ValueError:
        user_steps = 100

    GRID_SIZE = 250
    FUTURE_STEPS = 100

    # Generate environment with random seed
    forest = generate_clumpy_forest(GRID_SIZE, clump_scale=35, tree_ratio=0.5, seed=random_seed)
    city = generate_large_cluster_city_matrix(GRID_SIZE, forest, smoothness=50, distance_influence=0.2, center_bias=1.3)
    city_with_forest = city.copy()
    city_with_forest[forest == 1] = TREE

    fire_sim = FireGrid(city_with_forest)

    # Create figure for animation
    fig, ax = plt.subplots(figsize=(6, 6))  # Create a 6x6 inch figure
    imshow_obj = ax.imshow(fire_sim.grid, cmap="hot", vmin=-1, vmax=10)  # Display the grid, color-mapped with 'hot' colormap
    ax.axis('off')  # Turn off the axis for the visualization

    # Animation loop to simulate fire spread for a number of steps
    for step in range(user_steps):
        fire_sim.visualize(step, imshow_obj)  # Update the visualization to reflect the current fire grid
        fire_sim.step()  # Advance the fire simulation by one time step
        plt.title(f"Fire Spread Step {step}")  # Update the title of the plot to reflect the current step
        plt.pause(0.01)  # Pause to display the updated plot for a brief moment (this controls animation speed)

    plt.close(fig)  # 👈 Closes the fire animation window after it's done

    # 🔥 Compute population-weighted future fire danger
    pop_fire_danger = np.zeros_like(fire_sim.grid, dtype=float)
    burn_frequency = np.zeros_like(fire_sim.grid, dtype=float)

    for _ in range(FUTURE_STEPS):
        fire_sim.step()
        burning_now = (fire_sim.grid == FIRE)
        
        # Add population-weighted burning to danger
        pop_fire_danger += burning_now * city
        burn_frequency += burning_now.astype(float)

    # Normalize all components
    fire_component = normalize(pop_fire_danger)         # 🔥 Most important
    forest_component = normalize((forest == 1).astype(float))
    city_component = normalize(city.astype(float))

    # ⚖️ weight of things burned
    total_danger = (
        1.5 * fire_component +     # 🔥 population burned 
        1 * forest_component +   # 🌲 forest presence 
        0.75 * city_component       # 🏙 overall population 
    )

    # ✅ Normalize final danger matrix before scaling
    normalized_total_danger = normalize(total_danger)
    scaled_danger = np.round(normalized_total_danger * 9).clip(0, 9).astype(int)

    # Final display
    plt.figure(figsize=(6, 6))
    plt.imshow(scaled_danger, cmap="inferno", interpolation="nearest")
    plt.title("Predicted Fire Danger Map (Next 100 Steps)")
    plt.axis("off")
    plt.colorbar(label="Danger Level (0–9)")
    plt.show()

    return scaled_danger, fire_sim.fire_time, city, forest

# Run if standalone
if __name__ == "__main__":
    danger_map, fire_timeline, city, forest = predict_fire_threat()