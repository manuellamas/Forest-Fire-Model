import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import random
import copy # For list deepcopy

import time # Measuring run rime


"""
Coordinates are Matrix like

Point (1,0) is line 1 and column 0

__
P_

X coordinate is vertical, from top to bottom
Y coordinate is horizontal, from left to right

"""


# Setting seed
# random.seed(42)


def random_cell(w,h):
    """ Returns coordinates of random cell, given the map limits """
    return random.randint(0, h - 1), random.randint(0, w - 1)


def get_neighbors(cell_map, cell, w, h):
    """ Returns list of given cell neighbors' coordinates """
    neighbors = []

    x, y = cell


    # Going by vertical borders, and within those horizontal borders

    if cell[0] == 0: # TOP
        if cell[1] == 0: # LEFT
            neighbors.append((x+1, y)) # Below
            neighbors.append((x+1, y+1)) # Below Right
            neighbors.append((x, y+1)) # Right

        elif cell[1] == w - 1: # RIGHT
            neighbors.append((x+1, y)) # Below
            neighbors.append((x+1, y-1)) # Below Left
            neighbors.append((x, y-1)) # Left
        
        else:
            neighbors.append((x+1, y-1)) # Below Left
            neighbors.append((x+1, y)) # Below
            neighbors.append((x+1, y+1)) # Below Right
            neighbors.append((x, y-1)) # Left
            neighbors.append((x, y+1)) # Right


    elif cell[0] == h - 1: # BOT
        if cell[1] == 0: # LEFT
            neighbors.append((x-1, y)) # Above
            neighbors.append((x-1, y+1)) # Above Right
            neighbors.append((x, y+1)) # Right

        elif cell[1] == w - 1: # RIGHT
            neighbors.append((x-1, y)) # Above
            neighbors.append((x-1, y-1)) # Above Left
            neighbors.append((x, y-1)) # Left
        
        else:
            neighbors.append((x-1, y-1)) # Above Left
            neighbors.append((x-1, y)) # Above
            neighbors.append((x-1, y+1)) # Above Right
            neighbors.append((x, y-1)) # Left
            neighbors.append((x, y+1)) # Right
    
    else:
        if cell[1] == 0: # LEFT
            neighbors.append((x+1, y)) # Below
            neighbors.append((x+1, y+1)) # Below Right
            neighbors.append((x, y+1)) # Right
            neighbors.append((x-1, y+1)) # Above Right
            neighbors.append((x-1, y)) # Above

        elif cell[1] == w - 1: # RIGHT
            neighbors.append((x-1, y)) # Above
            neighbors.append((x-1, y-1)) # Above Left
            neighbors.append((x, y-1)) # Left
            neighbors.append((x+1, y-1)) # Below Left
            neighbors.append((x+1, y)) # Below
        
        else:
            neighbors.append((x-1, y+1)) # Above Right
            neighbors.append((x-1, y)) # Above
            neighbors.append((x-1, y-1)) # Above Left
            neighbors.append((x, y-1)) # Left
            neighbors.append((x+1, y-1)) # Below Left
            neighbors.append((x+1, y)) # Below
            neighbors.append((x+1, y+1)) # Below Right
            neighbors.append((x, y+1)) # Right
    
    
    return neighbors


#################
# Main function #
#################

def forestFireModel(g):
    tree_spawning_p = g
    lightnining_p = 1 - tree_spawning_p

    num_iterations = 3_000
    WIDTH = 75
    HEIGHT = 50

    # Colors for the different states
    EMPTY = [0, 0, 0]
    TREE = [0, 255, 0]
    BURN = [255, 0, 0]

    # np.random.seed(42)

    # cell_map_empty = [[[0, 0, 0] for j in range(HEIGHT)] for i in range(WIDTH)]
    # cell_map_empty = np.array([[[0, 0, 0] for j in range(HEIGHT)] for i in range(WIDTH)]) # Numpy arrays allow for reading values as list1[0,1,2] instead of list1[0][1][2]
    cell_map_empty = np.array([[EMPTY for j in range(WIDTH)] for i in range(HEIGHT)]) # Numpy arrays allow for reading values as list1[0,1,2] instead of list1[0][1][2]
    
    # Instead of [0,0,0] create a class for cell, and have two things, state, and color (This would require two "runs" one to change the state, and a second to change color)
    # Ooooor create a function that reads color (rgb triplet, according to the colors I've chosen) and tells us the state (Empty or Forest)


    # Make a deep copy of the above list
    cell_map = copy.deepcopy(cell_map_empty)

    # The Figure
    plt.style.use('dark_background')
    fig, ax = plt.subplots()



    # Keeping track of burning trees, these burn for one period, but even when burning they can become other trees
    burning_trees = []


    def update_plot(n, cell_map, burning_trees):
        ax.clear() # Clear/reset image

        old_cell_map = copy.deepcopy(cell_map) # A new one needs to be created so that the changes are made all at the same time


        # Randomly chosen cell
        chosen_cell = random_cell(WIDTH, HEIGHT)

        num_burn_trees = len(burning_trees)

        for i in range(num_burn_trees):
            tree = burning_trees.pop()

            ## Burn neighbors

            # Get list of neighbors
            neighbors = get_neighbors(cell_map, tree, WIDTH, HEIGHT)
            
            for neighbor in neighbors: # Neighbors of burning trees burn
                if (old_cell_map[tuple(neighbor)] == TREE).all():
                    cell_map[tuple(neighbor)] = BURN
                    burning_trees.insert(0, tuple(neighbor)) # Push new tree at the beginning of the list (queue)


            ## Burning trees stop burning (and can in the same period become trees again)
            cell_map[tuple(tree)] = EMPTY # tuple allows for being read as input in a numpy array


        # If site has a tree
        if (old_cell_map[chosen_cell] == TREE).all(): # .all() checks if both arrays are equal
            random_num = random.random()

            if random_num <= lightnining_p: # Lightning strikes and tree burns
                cell_map[chosen_cell] = BURN
                burning_trees.insert(0, chosen_cell) # Push new tree at the beginning of the list (queue)

        # If site is empty
        elif (old_cell_map[chosen_cell] == EMPTY).all(): # .all() checks if both arrays are equal
            random_num = random.random()

            if random_num <= tree_spawning_p: # Tree spanws
                cell_map[chosen_cell] = TREE

        else: # No other state because if it was burning it no longer is, due to the for cycle above
            pass


        img = cell_map

        # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.imshow.html#matplotlib.axes.Axes.imshow
        ax.imshow(img)

        ax.set_title(f"frame {n}")

        return cell_map, burning_trees


    ani = animation.FuncAnimation(fig, update_plot, num_iterations, fargs = (cell_map, burning_trees), interval = 1, repeat = False) # Interval defines the delay between frames in miliseconds (smaller value means a smaller duration and thus faster)
    # ani = animation.FuncAnimation(fig, update_plot, num_iterations, fargs = (cell_map, burning_trees), interval = 300, repeat = False) # Interval defines the delay between frames in miliseconds (smaller value means a smaller duration and thus faster)

    ani.save("Forest_fire_Model.mp4") # Make sure to create the folder before running
    # ani.save("Plot_animations\\Forest_fire_Model" + "" + ".mp4") # Make sure to create the folder before running
    # plt.show()




start = time.time()

forestFireModel(0.95)

print("Running Time")
print(time.time() - start)