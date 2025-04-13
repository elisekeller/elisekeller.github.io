import numpy as np
import matplotlib.pyplot as plt

# Constants for visualization
TREE = -1
FIRE = 100  # Arbitrary high value that won't overlap population values

# Parameters (default values)
GRID_SIZE = 250
TREE_SPREAD_PROB = 0.35
EMPTY_SPREAD_PROB = 0.02
SPREAD_DENSITY_SCALE = 0.55  # Tune this value to control influence of population density
BURN_DURATION = 10
DEFAULT_STEPS = 250

def wind_vector_components(angle_degrees):
    """Convert angle in degrees (0 = right, 90 = up) to normalized (dy, dx)."""
    radians = np.radians(angle_degrees)
    return -np.sin(radians), np.cos(radians)

class FireGrid:
    def __init__(self, forest_city_matrix):
        self.grid = forest_city_matrix.copy()
        self.fire_time = np.zeros_like(self.grid, dtype=int)

        # Find a TREE to ignite
        tree_indices = np.argwhere(self.grid == TREE)

        # Check if tree_indices is empty
        if len(tree_indices) == 0:
            raise ValueError("No trees found in the city matrix. Ensure that your city matrix contains trees marked by the TREE constant.")

        # Randomly select a tree to ignite
        y, x = tree_indices[np.random.choice(len(tree_indices))]  # Randomly select a tree to ignite
        self.grid[y, x] = FIRE
        self.fire_time[y, x] = 1

    def step(self):
        new_grid = self.grid.copy()
        new_fire_time = self.fire_time.copy()

        fire_yx = np.argwhere(self.grid == FIRE)
        for y, x in fire_yx:
            # Burned out?
            if self.fire_time[y, x] >= BURN_DURATION:
                new_grid[y, x] = 0  # Becomes EMPTY
                new_fire_time[y, x] = 0
                continue

            new_fire_time[y, x] += 1

            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < self.grid.shape[0] and 0 <= nx < self.grid.shape[1]:
                        target = self.grid[ny, nx]

                        # Spread fire to trees
                        if target == TREE and np.random.random() < TREE_SPREAD_PROB:
                            new_grid[ny, nx] = FIRE
                            new_fire_time[ny, nx] = 1
                        # Spread fire to non-tree areas based on population density
                        elif target != FIRE and target != TREE:
                            # Calculate spread probability based on population density
                            population_density = self.grid[ny, nx]
                            if population_density == 0:
                                prob = EMPTY_SPREAD_PROB  # Regular empty land
                            else:
                                # Slightly increase spread probability based on population density
                                prob = EMPTY_SPREAD_PROB * (1 + population_density * SPREAD_DENSITY_SCALE)

                            if np.random.random() < prob:
                                new_grid[ny, nx] = FIRE
                                new_fire_time[ny, nx] = 1

        self.grid = new_grid
        self.fire_time = new_fire_time

    def visualize(self, step, imshow_obj):
        # Prepare grid for display
        display_grid = self.grid.copy()
        display_grid[display_grid == TREE] = -1
        display_grid[display_grid == FIRE] = 10  # Just a high value to make it visibly distinct

        # Update the imshow object with the new grid data
        imshow_obj.set_array(display_grid)

    def get_final_grid(self):
        return self.grid

# EXAMPLE USAGE
if __name__ == '__main__':
    from Forest import generate_clumpy_forest, TREE as TREE_MARKER
    from Forest_City import generate_large_cluster_city_matrix  # Assuming your city generator is in City.py

    # Allow user input for the number of steps
    user_steps = input(f"Enter the number of timesteps (default is {DEFAULT_STEPS}): ")
    steps = int(user_steps) if user_steps.isdigit() else DEFAULT_STEPS

    # Build forest-city combo matrix
    forest = generate_clumpy_forest(GRID_SIZE, clump_scale=35, tree_ratio=0.5)
    forest_city = generate_large_cluster_city_matrix(GRID_SIZE, forest, smoothness=50, distance_influence=0.2, center_bias=1.3)

    # Initialize the fire simulation
    fire_sim = FireGrid(forest_city)

    # Create the figure and initial imshow object
    fig, ax = plt.subplots(figsize=(6, 6))
    imshow_obj = ax.imshow(fire_sim.grid, cmap="hot", vmin=-1, vmax=10)
    ax.axis('off')

    # Run the animation loop and visualize each step
    for step in range(steps):
        fire_sim.visualize(step, imshow_obj)
        fire_sim.step()
        plt.title(f"Fire Spread Step {step}")
        plt.pause(0.01)  # Control the speed of the animation (increase if too fast)

    # After all steps, return the final grid (this is the final matrix)
    final_matrix = fire_sim.get_final_grid()

    # Display the final matrix after the simulation ends
    plt.figure(figsize=(6, 6))
    plt.imshow(final_matrix, cmap="hot", vmin=-1, vmax=10)
    plt.title(f"Final Fire Spread Matrix after {steps} Steps")
    plt.axis('off')  # Hide axes for cleaner visualization
    plt.show()

    # Return the final grid for further analysis or processing
    print("Final fire spread matrix (last timestep):")
    print(final_matrix)