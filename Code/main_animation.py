# For plot and animation
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


def random_cell(w,h):
    """ Returns coordinates of random cell, given the map limits """
    return random.randint(0, h - 1), random.randint(0, w - 1)


def get_neighbors(cell_map, cell, w, h):
    """ Returns list of given cell neighbors' coordinates """
    neighbors = []

    x, y = cell

    RIGHT = (x, y+1)
    LEFT = (x, y-1)
    
    BELOW = (x+1, y)
    BELOW_RIGHT = (x+1, y+1)
    BELOW_LEFT = (x+1, y-1)
    
    ABOVE = (x-1, y)
    ABOVE_RIGHT = (x-1, y+1)
    ABOVE_LEFT = (x-1, y-1)

    # Going by vertical borders, and within those horizontal borders

    if cell[0] == 0: # TOP
        if cell[1] == 0: # LEFT
            neighbors.append(BELOW)
            neighbors.append(BELOW_RIGHT)
            neighbors.append(RIGHT)

        elif cell[1] == w - 1: # RIGHT
            neighbors.append(BELOW)
            neighbors.append(BELOW_LEFT)
            neighbors.append(LEFT)
        
        else:
            neighbors.append(BELOW_LEFT)
            neighbors.append(BELOW)
            neighbors.append(BELOW_RIGHT)
            neighbors.append(LEFT)
            neighbors.append(RIGHT)


    elif cell[0] == h - 1: # BOT
        if cell[1] == 0: # LEFT
            neighbors.append(ABOVE)
            neighbors.append(ABOVE_RIGHT)
            neighbors.append(RIGHT)
            

        elif cell[1] == w - 1: # RIGHT
            neighbors.append(ABOVE)
            neighbors.append(ABOVE_LEFT)
            neighbors.append(LEFT)
        
        else:
            neighbors.append(ABOVE_LEFT)
            neighbors.append(ABOVE)
            neighbors.append(ABOVE_RIGHT)
            neighbors.append(LEFT)
            neighbors.append(RIGHT)
    
    else: # Not on the top or bottom edge
        if cell[1] == 0: # LEFT
            neighbors.append(BELOW)
            neighbors.append(BELOW_RIGHT)
            neighbors.append(RIGHT)
            neighbors.append(ABOVE_RIGHT)
            neighbors.append(ABOVE)


        elif cell[1] == w - 1: # RIGHT
            neighbors.append(ABOVE)
            neighbors.append(ABOVE_LEFT)
            neighbors.append(LEFT)
            neighbors.append(BELOW_LEFT)
            neighbors.append(BELOW)
        
        else:
            neighbors.append(ABOVE_RIGHT)
            neighbors.append(ABOVE)
            neighbors.append(ABOVE_LEFT)
            neighbors.append(LEFT)
            neighbors.append(BELOW_LEFT)
            neighbors.append(BELOW)
            neighbors.append(BELOW_RIGHT)
            neighbors.append(RIGHT)

    
    return neighbors


#################
# Main function #
#################

def forestFireModel(g, num_iterations = 3_000, dimensions = (75, 50), save = True, seed_value = None):
    """
    
    g
    - g probability of spawning tree if chosen cell is empty
    - 1-g probability of lightning striking chosen cell if it contains a tree

    num_iterations
    - number of periods/frames

    save
    - save to MP4 file if True
    - show only (while running) if False

    seed_value
    - if a value is given it's the seed used for random operations
    - else a random seed is used (time)
    
    """

    # Running time
    start = time.time()
    last_time = 0

    # Setting seed
    if seed_value is not None:
        random.seed(seed_value)
        # np.random.seed(42)

    # Probabilities
    tree_spawning_p = g
    lightnining_p = 1 - tree_spawning_p

    # Dimensions
    WIDTH = dimensions[0]
    HEIGHT = dimensions[1]

    # Colors for the different states
    EMPTY = [0, 0, 0]
    TREE = [0, 255, 0]
    BURN = [255, 0, 0]


    # Initializing map as all EMPTY
    cell_map = np.array([[EMPTY for j in range(WIDTH)] for i in range(HEIGHT)]) # Numpy arrays allow for reading values as list1[0,1,2] instead of list1[0][1][2]
    
 
    # The Figure
    plt.style.use('dark_background')
    fig, ax = plt.subplots()


    # Keeping track of burning trees, these burn for one period, but even when burning they can become other trees
    burning_trees = []




    def update_plot(n, cell_map, burning_trees):
        """ Updates image at each frame """
        
        nonlocal last_time # So that we can change last_time value even though it's in the outer function's scope

        cur_sec = int(time.time() - start)

        # Some feedback to know the code is running "ok"
        if save and (cur_sec > last_time):
            last_time += 1
            if cur_sec % 10 == 0:
                # print(cur_sec, last_time)
                # print(n)
                print(cur_sec)


        ax.clear() # Clear/reset image


        ########
        # Main #
        ########

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


        ##################
        # Creating Frame #
        ##################

        # Create the image for the frame
        ax.imshow(cell_map)

        # Set the title (for each frame)
        ax.set_title(f"Period {n}")

        return cell_map, burning_trees



    # Produces animation
    # Interval, 5 is too fast to see the "burn", 15 is ok-ish, 25 seems to give the best experience without being too slow
    interval_ms = 25
    ani = animation.FuncAnimation(fig, update_plot, num_iterations, fargs = (cell_map, burning_trees), interval = interval_ms, repeat = False) # Interval defines the delay between frames in miliseconds (smaller value means a smaller duration and thus faster)


    if save: # Saves to a mp4 file
        ani.save("Forest_fire_model.mp4") # Make sure to create the folder before running
        # ani.save("Forest_fire_model" + str(interval_ms) + ".mp4") # Make sure to create the folder before running
        # ani.save("Plot_animations\\Forest_fire_Model" + "" + ".mp4") # Make sure to create the folder before running

    else: # Presents (as it runs)
        plt.show()

    # Running time
    print("Final Running Time")
    print(time.time() - start)



# forestFireModel(0.95, num_iterations = 3_000, save = False)
forestFireModel(0.95, num_iterations = 3_000, save = True)
