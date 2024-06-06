import numpy as np
import matplotlib.pyplot as plt
import random

class Ant:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state  # "search" or "return"

grid_size = 10
num_ants = 5

# Constants
ANTHILL = 1
FOOD = 2

# Initialization
def initialize():
    grid = np.zeros((grid_size, grid_size))
    nest_pheromones = np.ones((grid_size, grid_size))
    food_pheromones = np.ones((grid_size, grid_size))

    grid[0, 0] = ANTHILL
    grid[4, 4] = FOOD

    ants = []
    for _ in range(num_ants):
        ants.append(Ant(0, 0, "search"))  # Ants start at the anthill

    return grid, nest_pheromones, food_pheromones, ants

# Decision Making
def move_ant(ant, grid, nest_pheromones, food_pheromones):
    x, y = ant.x, ant.y
    if ant.state == "search":
        pheromone_levels = {
            "up": food_pheromones[max(y - 1, 0), x],
            "down": food_pheromones[min(y + 1, grid_size - 1), x],
            "left": food_pheromones[y, max(x - 1, 0)],
            "right": food_pheromones[y, min(x + 1, grid_size - 1)]
        }

    elif ant.state == "return":
        pheromone_levels = {
            "up": nest_pheromones[max(y - 1, 0), x],
            "down": nest_pheromones[min(y + 1, grid_size - 1), x],
            "left": nest_pheromones[y, max(x - 1, 0)],
            "right": nest_pheromones[y, min(x + 1, grid_size - 1)]
        }

    total_pheromone = sum(pheromone_levels.values())
    if total_pheromone > 0:
        for direction in pheromone_levels:
            pheromone_levels[direction] /= total_pheromone
    else:
        pheromone_levels = {direction: 1.0 / len(pheromone_levels) for direction in pheromone_levels}

    direction = random.choices(["up", "down", "left", "right"], weights=list(pheromone_levels.values()))[0]

    if direction == "up":
        ant.y = max(ant.y - 1, 0)
    elif direction == "down":
        ant.y = min(ant.y + 1, grid_size - 1)
    elif direction == "left":
        ant.x = max(ant.x - 1, 0)
    elif direction == "right":
        ant.x = min(ant.x + 1, grid_size - 1)

    # Update state if the ant reaches the food or anthill
    if ant.state == "search" and grid[ant.y, ant.x] == FOOD:
        ant.state = "return"
    elif ant.state == "return" and grid[ant.y, ant.x] == ANTHILL:
        ant.state = "search"

# Update Pheromones (with decay)
def update_pheromones(ants, nest_pheromones, food_pheromones, decay_rate=0.9):
    nest_pheromones *= decay_rate
    food_pheromones *= decay_rate

    for ant in ants:
        if ant.state == "search":
            nest_pheromones[ant.y, ant.x] += 1
        elif ant.state == "return":
            food_pheromones[ant.y, ant.x] += 1

# Plotting
def visualize_grid(grid, ants):
    plt.clf()  # Clear the previous plot
    cmap = plt.cm.get_cmap('viridis', 3)  # Colormap with 3 distinct colors
    plt.imshow(grid, interpolation='none', cmap=cmap)
    plt.colorbar()

    for ant in ants:
        color = 'red' if ant.state == "search" else 'blue'
        plt.scatter(ant.x, ant.y, color=color)

    plt.pause(0.05)  # Slight pause for visualization

# Main Loop
grid, nest_pheromones, food_pheromones, ants = initialize()

plot_limit = 25
plot_count = 0

while plot_count < plot_limit:  # Change the limit as needed
    for ant in ants:
        move_ant(ant, grid, nest_pheromones, food_pheromones)
    update_pheromones(ants, nest_pheromones, food_pheromones)
    visualize_grid(grid, ants)
    plot_count += 1

plt.show()  # Show the final plot