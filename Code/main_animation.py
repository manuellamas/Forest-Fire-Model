import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import random
import copy # For list deepcopy


# Setting seed
# random.seed(42)


def random_cell(w,h):
    return random.randint(0, w - 1), random.randint(0, h - 1)




#################
# Main function #
#################

def forestFireModel(g):
    tree_spawning_p = g
    lightnining_p = 1 - tree_spawning_p

    num_iterations = 500
    WIDTH = 50
    HEIGHT = 50

    # Colors for the different states
    EMPTY = [0, 0, 0]
    TREE = [0, 255, 0]
    BURN = [255, 0, 0]

    # np.random.seed(42)

    # cell_map_empty = [[[0, 0, 0] for j in range(HEIGHT)] for i in range(WIDTH)]
    # cell_map_empty = np.array([[[0, 0, 0] for j in range(HEIGHT)] for i in range(WIDTH)]) # Numpy arrays allow for reading values as list1[0,1,2] instead of list1[0][1][2]
    cell_map_empty = np.array([[EMPTY for j in range(HEIGHT)] for i in range(WIDTH)]) # Numpy arrays allow for reading values as list1[0,1,2] instead of list1[0][1][2]
    
    # Instead of [0,0,0] create a class for cell, and have two things, state, and color (This would require two "runs" one to change the state, and a second to change color)
    # Ooooor create a function that reads color (rgb triplet, according to the colors I've chosen) and tells us the state (Empty or Forest)


    # Make a deep copy of the above list
    cell_map = copy.deepcopy(cell_map_empty)

    # The Figure
    plt.style.use('dark_background')
    fig, ax = plt.subplots()



    # Keeping track of burning trees, these burn for one period, but even when burning they can become other trees
    burning_trees = []


    def update_plot(n, cell_map, teatet):
        ax.clear() # Clear/reset image

        print(n, cell_map[1])
        old_cell_map = copy.deepcopy(cell_map) # A new one needs to be created so that the changes are made all at the same time

        print(cell_map)

        # Randomly chosen cell
        chosen_cell = random_cell(WIDTH, HEIGHT)

        for tree in burning_trees:
            ## Burn neighbors
            
            # Get list of neighbors

            ## Burning trees stop burning (and can in the same period become trees again)
            cell_map[tuple(tree)] = EMPTY # tuple allows for being read as input in a numpy array


        # If site has a tree
        if (old_cell_map[chosen_cell] == TREE).all(): # .all() checks if both arrays are equal
            random_num = random.random()

            if random_num >= lightnining_p: # Lightning strikes and tree burns
                cell_map[chosen_cell] = BURN
                burning_trees.append([chosen_cell])
            

        # If site is empty
        elif (old_cell_map[chosen_cell] == EMPTY).all(): # .all() checks if both arrays are equal
            random_num = random.random()

            if random_num >= tree_spawning_p: # Tree spanws
                cell_map[chosen_cell] = TREE

        else:
            pass

        # img = data[n]
        img = cell_map

        # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.imshow.html#matplotlib.axes.Axes.imshow
        ax.imshow(img)
        print(cell_map)

        ax.set_title(f"frame {n}")
        cell_map[1] += 1
        return cell_map


    ani = animation.FuncAnimation(fig, update_plot, num_iterations, fargs = (cell_map, 0), interval = 150, repeat = False) # Interval defines the speed of the animation (smaller value means a smaller duration and thus faster) and it works regardless the number of frames (iterations)
    # ani = animation.FuncAnimation(fig, update_plot, num_iterations, fargs = (cell_map), interval = 150, repeat = False) # Interval defines the speed of the animation (smaller value means a smaller duration and thus faster) and it works regardless the number of frames (iterations)

    # ani.save("Plot_animations\\Forest_fire_Model" + "" + ".mp4") # Make sure to create the folder before running
    plt.show()


forestFireModel(0.5)