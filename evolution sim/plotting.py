import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
print(matplotlib.__version__)
def plot(x_axis_list,y_axis_list,xlabel,ylabel):
    plt.figure(figsize=(4, 3), dpi=200)
    plt.clf()
    x_point = np.array(x_axis_list)
    y_point = np.array(y_axis_list)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.plot(x_point,y_point)

    plt.tight_layout()

    plt.savefig(f"{ylabel}plot.png")
    plt.close()
x_list = []
y_list = []

