---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---

<center><h1> Enhancing Wildfire Response Through Quantum Optimization </h1></center>
Welcome to Qooked! Our team has developed a platform to better understand and simulate the spread of wildfires. In partnership with Tahoe-Quantum, we created an algorithm that predicts how fires are likely to move based on terrain and population density. This helps determine where emergency responders are needed most. Our goal is to offer an innovative tool that not only saves money—but most importantly, saves lives.

---

<h2 style="padding-top: 25px;">About Us</h2>

Our team is composed of four undergraduate students—two from Boston University and two from Brandeis University. United by a shared passion for quantum computing, we took on this challenge with the goal of using our knowledge to make a meaningful, progressive impact on the world.

---

<h2 style="padding-top: 25px;">QUBO Formulation: Structuring the Optimization Problem</h2>
Before diving into the quantum aspect of our work, we first focused on optimizing the problem using a QUBO formulation. A QUBO (Quadratic Unconstrained Binary Optimization) is a way of representing an optimization problem using binary variables. It's commonly used in areas like scheduling, graph analysis, and, in our case, resource allocation. By incorporating penalties for placing resources too close together, the QUBO helps us model important constraints and make more strategic decisions about where support is most needed.

---

<h2 style="padding-top: 25px;">From QUBO to Quantum: Solving with the Ising Model</h2>
The quantum component of our project lies in the optimization of the QUBO. We convert the QUBO into an Ising model, a form that’s better suited for computation on quantum hardware. The Ising model represents the problem using spins, external fields, and couplings between variables. A quantum annealer then explores all possible combinations of binary variables by placing them into a superposition of 0s and 1s. 

Unlike classical computers, which must evaluate each combination one at a time, quantum systems can consider all configurations at once. This ability to process many possibilities in parallel is what makes quantum computing so powerful, especially for large-scale simulations, where classical methods become exponentially slower.

---

<h2 style="padding-top: 25px;">Simulating Wildfires and Optimizing Response</h2>

We separated our challenge into two separate parts to best utilize an effective method in which quantum computing will help to determine the proper course of action in preventing wildfires. 

### Simulating Fire Spread

The first phase of our method involves simulating a wildfire scenario, by accurately plotting a randomly generated city and collection of forests/arid material using a matrix. The cities are represented by a population density from integers 0 to 7, and distributed so that denser cells were are likely to originate next to each other, and away from forest/arid material. 

After creating a matrix, we can run the simulation of fire spreading from a randomly determined forest origin. The probability of adjacent cells catching fire is determined by their weight in population density and material (arid material or not). Increased density and arid material increase the probability of fire spread to simulate how largely dense areas tend to increase fire propagation. 

Our main program, Firethreat.py, allows one to create a random city, run the simulation of fire spread for n timesteps, and then return the most dangerous areas predicted in the next 100 timesteps as a heatmap. 

### Quantum Optimization
With the simulation complete, this final heatmap matrix can be run through our quantum simulation to produce a minimized binary matrix that represents the most optimal location and allocation of resources, targeting the most at-risk areas with maximal efficiency.

---

<h2 style="padding-top: 25px;">Real-World Applications and Future Potential</h2>

Effectively, a practical implementation of this type of program would be able to map to actual real world cities or counties, select the origin point of a wildfire, find the most dangerous areas to be affected, and return the most efficient allocation of resources. A fully implemented client program could further scout for more in depth variables such as topographical area, weather conditions, humidity, and wind speeds, which all further affect fire propagation.

---














<center><h1 style="padding-top: 50px;">Fire Spread Analysis and Optimization Results</h1></center>

<h2 style="padding-top: 25px;">1: Simulating a City and Environment</h2>
We first create a synthetic environment using city_generator.py and Forest.py. Cities are represented as matrices with population densities ranging from 0 to 7, while forests and arid materials are scattered throughout the grid.
The result is a synthetic but realistic environment with both urban and wildland areas, providing the foundation for simulating how a fire might behave.

```python
def generate_large_cluster_city_matrix(size, forest_matrix, smoothness=10.0, distance_influence=2.0, center_bias=2.0):
    """
    Generates a city layout matrix with population density favorably distributed:
    -1 = TREE (unbuildable)
    0  = buildable but unpopulated
    1–8 = increasing levels of population density
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
    dist_to_center = np.sqrt((x - center_x)2 + (y - center_y)2)
    center_bias_map = 1 - (dist_to_center / dist_to_center.max())  # 1 at center, 0 at corners

    # Step 4: Normalize input maps
    smoothed_norm = (smoothed - smoothed.min()) / (smoothed.max() - smoothed.min())
    distance_norm = (distance_map - distance_map.min()) / (distance_map.max() - distance_map.min())

    # Step 5: Combine factors
    biased_density = smoothed_norm * (distance_norm  distance_influence) * (center_bias_map  center_bias)

    # Step 6: Scale to 1–8, threshold very low values to 0 (no pop), and set trees to -1
    scaled_density = (biased_density / biased_density.max()) * 8
    city_matrix = scaled_density.astype(int)
    city_matrix[city_matrix < 1] = 0         # No population
    city_matrix[tree_mask] = -1              # Forest cells

    return city_matrix
```


---

<h2 style="padding-top: 25px;">2: Simulating Fire Spread Over Time</h2>
Next, we ignite a fire at a randomly selected forest location. The fire spreads across the matrix over a series of timesteps. Whether a cell catches fire depends on its surrounding conditions — densely populated areas and nearby forests are more likely to ignite. This spreading process is repeated frame-by-frame to visualize how the fire grows. 

```python
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
```

The output is an animated sequence that shows the progression of fire over time, revealing how it moves more rapidly through forests and densely populated zones. These patterns highlight high-risk areas and provide crucial insight for optimizing emergency response strategies.

![Fire Spread](/images/image3.gif){:width="500"}


---

<h2 style="padding-top: 25px;">3: Mapping Future Risk with a Heatmap</h2>
To anticipate where the fire is most likely to go, we run the fire spread simulation many times and record how often each cell ignites. The result is a heatmap that shows the probability of fire impact over time.
Brighter areas on the heatmap indicate locations that are consistently affected by fire across simulations. This heatmap is then used as input for the optimization step, serving as a probability-based model of where fire poses the greatest threat.

```python
# Normalize final danger matrix before scaling
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
```

This heatmap reveals the most dangerous regions in the next 100 timesteps and serves as a probability-based model of future fire impact. Areas with higher values indicate both greater flammability and a higher likelihood of sustained fire activity, often due to the combination of high population density and forest coverage.

<img src="/images/image1.png" alt="Predicted Fire Danger Map (Next 100 Steps)" width="500">

This output becomes the foundation for the next stage—optimizing where to allocate firefighting resources for maximum effectiveness.

---

<h2 style="padding-top: 25px;">4: Optimizing Resource Deployment with Quantum Computing</h2>
Using the heatmap, we build an optimization problem to determine the best locations for emergency responders. Our goal is to place the fewest units possible while still covering all high-risk areas. To do this, we convert the problem into a Quadratic Unconstrained Binary Optimization (QUBO) model.
We also include a penalty that discourages placing units too close together, ensuring wide coverage across the map. This QUBO model is then solved using quantum-inspired algorithms, such as simulated annealing, to find an efficient deployment strategy. The output is a binary matrix showing the optimal responder placements. 

```python
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
    H += float(alpha).float() * total_selected

    # Penalty for adjacent units selected together
    if allow_adjacent_penalty:
        for i in range(n):
            for j in range(n):
                if i < n - 1:
                    H += float(beta).float() * variables[(i, j)] * variables[(i + 1, j)]
                if j < n - 1:
                    H += float(beta).float() * variables[(i, j)] * variables[(i, j + 1)]

    model = H.compile()
    qubo, offset = model.to_qubo()
    return qubo, offset, model
```

```python
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
```

---

<h2 style="padding-top: 25px;">5: Comparing Optimization Results</h2>
To demonstrate the effectiveness of the quantum optimization, we compare the QUBO-based responder placement to a simpler baseline strategy, such as uniformly distributing units across the grid. The quantum-optimized layout typically requires fewer responders while offering better coverage of high-risk zones, making it a more efficient and targeted solution.

The visual comparison shows how the deployment changes based on risk concentration rather than arbitrary spacing. These changes are derived from our heatmap 100 timesteps into the future and reflect the most strategic locations for dispatching first responders and aid.

```python
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
```

<h2 style="padding-top: 30px;"></h2>
<img src="/images/image2.png" alt="" width="800">
<h2 style="padding-top: 15px;"></h2>


Due to hardware limitations in both classical simulation and current quantum solvers, we reduce the original 250×250 heatmap to a manageable 50×50 matrix during optimization. However, full-scale quantum systems would be capable of solving the larger version in exponentially less time—demonstrating the potential scalability of this approach for real-world emergency logistics.




---

<center><h2 style="padding-top: 50px;">From Simulation to Real-World Impact</h2></center>

Wildfires continue to grow in frequency and severity—but so does our capacity to respond. Through this project, we’ve shown how quantum-inspired optimization and simulation can work together to model complex fire behavior, predict areas of greatest risk, and deploy resources with precision.

By combining detailed environmental modeling with advanced computing techniques like QUBO-based optimization, we are not only improving emergency planning but also exploring how next-generation technology can address urgent global challenges.

While this is a simulation, the tools and methodology are real—and scalable. With greater access to quantum hardware and real-world fire data, this framework could evolve into a powerful decision-making system used by first responders and public safety agencies.

We hope this work demonstrates how science and technology can come together to protect communities, environments, and lives in the face of natural disasters.
