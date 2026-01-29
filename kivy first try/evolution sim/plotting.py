import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
print(matplotlib.__version__)
def plot(x_axis_list,y_axis_list):

    x_point = np.array(x_axis_list)
    y_point = np.array(y_axis_list)

    plt.plot(x_point,y_point)
    plt.show()

x_list = []
y_list = []

