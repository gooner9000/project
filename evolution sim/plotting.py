import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
print(matplotlib.__version__)
def plot(x_axis_list,y_axis_list,xlabel,ylabel):
    """plots the graphs based on two lists given.
        One represents the X coordinates and the other the Y coordinates"""

    plt.figure(figsize=(4, 3), dpi=200)
    plt.clf()
    x_points = np.array(x_axis_list)
    y_points = np.array(y_axis_list)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.plot(x_points,y_points)

    plt.tight_layout()
    #saves the graph as a png file
    plt.savefig(f"{ylabel}plot.png")
    plt.close()
x_list = []
y_list = []

