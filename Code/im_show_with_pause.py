
# Testing a Matplotlib animation


import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
# data = np.random.random((50, 50, 50)) # One real number in the interval [0,1[
data = np.random.randint(0, 256, (50, 50, 50, 3)) # A triplet of integer numbers in range [0,255] (the high value is one above the actual maximum) https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html
# Number of frames, 

fig, ax = plt.subplots()

for i, img in enumerate(data):
    ax.clear()

    # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.imshow.html#matplotlib.axes.Axes.imshow
    ax.imshow(img)

    ax.set_title(f"frame {i}")
    # Note that using time.sleep does *not* work here!
    plt.pause(0.1)