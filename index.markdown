---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---

<center><h1> Enhancing Wildfire Response through Quantum Optimization </h1></center>
Welcome to Qooked! Our team has developed a platform to better understand and simulate the spread of wildfires. In partnership with Tahoe-Quantum, we created an algorithm that predicts how fires are likely to move based on terrain and population density. This helps determine where emergency responders are needed most. Our goal is to offer an innovative tool that not only saves money—but more importantly, saves lives.

---

## About Us:
Our team is composed of four undergraduate students—two from Boston University and two from Brandeis University. United by a shared passion for quantum computing, we took on this challenge with the goal of using our knowledge to make a meaningful, progressive impact on the world.

---

## Before the Quantum:
Before the quantum component of our work lies the optimization of the QUBO matrix. A QUBO matrix is a REPRESENTATION of an optimization problem, where the goal is to find the best combination of binary variables to minimize a quadratic function. QUBOs are often used for graph problems, scheduling, and what we have here, resource allocation. With a QUBO matrix, we penalize adjacent edges for more efficient coverage of an area, which creates negative weights on areas where resources need to be allocated. This allows us to represent the problem with various constraints that serve our interest.

---

## About the Quantum:
The Quantum component of our project lies in the optimization of the QUBO. The QUBO is converted into a Ising Model, which is essentially a form that is easier to compute with qubits. (It’s the summation of the spins, fields and couplings). The quantum annealer then superimposes the bits into all possible combinations of 0 and 1. This is the part that regular computers struggle with. They need to compute each combination individually, while quantum computers can compute every state simultaneously. Their fast speeds are why we applied quantum to this project, since with larger simulations and matrices it would take exponentially longer to compute them without a quantum computer. 

---

## How The Simulation Works:
We separated our challenge into two separate parts to best utilize an effective method in which quantum computing will help to determine the proper course of action in preventing wildfires. The first section of our method is simulation, accurately plotting a randomly generated city and collection of forests/arid material using a matrix. The cities were represented by a population density from integers 0 to 7, and distributed so that denser cells were more likely to originate next to each other and away from forest/arid material. After creating the matrix, we then ran a simulation of fire spreading from a randomly determined forest origin. The probability of adjacent cells catching fire was determined by their weight in population density and material (arid material or not). Increased density and arid material increased the probability of fire spread to simulate how largely dense areas tend to increase fire propagation. Our main program, Firethreat.py, would allow one to create a random city, run the simulation of fire spread for n timesteps, and then return the most dangerous areas predicted in the next 100 timesteps as a heatmap. With the simulation complete, this final heatmap matrix will be run through our quantum simulation to produce a minimized binary matrix that quickly represents the most optimal location and allocation of resources, covering the most needed area with the most efficient usage. Effectively, a practical implementation of this type of program would be able to map to actual real world cities or counties, select the origin point of a wildfire, find the most dangerous areas to be affected, and return the most efficient allocation of resources. A fully implemented client program could further scout for more in depth variables such as topographical area, weather conditions, humidity, and wind speeds, which all further affect fire propagation.





