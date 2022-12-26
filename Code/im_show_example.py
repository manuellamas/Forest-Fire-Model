import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

num_iterations = 200

np.random.seed(42)
data = np.random.randint(0, 256, (num_iterations, 50, 50, 3)) # A triplet of integer numbers in range [0,255] (the high value is one above the actual maximum) https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html






# The Figure
plt.style.use('dark_background')
fig, ax = plt.subplots()


def update_plot(n):
    ax.clear()

    img = data[n]
    print("\n\n\n---------------\nIMAGE\n--------------------\n\n\n\n")
    print(img)
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.imshow.html#matplotlib.axes.Axes.imshow
    ax.imshow(img)

    ax.set_title(f"frame {n}")



ani = animation.FuncAnimation(fig, update_plot, num_iterations, interval = 150, repeat = False) # Interval defines the speed of the animation (smaller value means a smaller duration and thus faster) and it works regardless the number of frames (iterations)
# ani = animation.FuncAnimation(fig, update_plot, num_iterations, fargs=(point, line), interval = 60, repeat = False)

# ani.save("Plot_animations\\Portugal_daily_new_cases_" + str(dates[-1]) + ".mp4") # Make sure to create the folder before running
plt.show()

