---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---

<center><h1> Enhancing Wildfire Response through Quantum Optimization </h1></center>
Welcome to Qooked! Our team has developed a platform to better understand and simulate the spread of wildfires. In partnership with Tahoe-Quantum, we created an algorithm that predicts how fires are likely to move based on terrain and population density. This helps determine where emergency responders are needed most. Our goal is to offer an innovative tool that not only saves money—but more importantly, saves lives.

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

<h2 style="padding-top: 10px;"></h2>
<img src="/images/image1.png" alt="Predicted Fire Danger Map (Next 100 Steps)" width="400">

Heatmap of Wildfire Spread 100 timesteps into the future; distribution determines the most dangerous future cells with respect to the cell value (The population density of that cell)

---

<h2 style="padding-top: 30px;"></h2>
<img src="/images/image2.png" alt="" width="800">
<h2 style="padding-top: 15px;"></h2>

Heatmap changes that reflect where the Optimized Deployment of first responders and aid should be 100 timesteps into the future. Due to limitations of quantum simulation/classical computing, the original heatmap must be reduced down to a 50x50 matrix. Quantum computing could find the optimal solution on the 250x250 in exponentially less time.

---

<h2 style="padding-top: 10px;"></h2>
![yay](/images/image3.gif){:width="400"}


Animation of how fire spreads through forest and populated territory. Simulates resistance from low density areas in comparison to the faster growth in forests and high population density locations





