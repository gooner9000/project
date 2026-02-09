import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
print(matplotlib.__version__)
def plot(x_axis_list,y_axis_list,xlabel,ylabel):

    x_point = np.array(x_axis_list)
    y_point = np.array(y_axis_list)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.plot(x_point,y_point,linestyle = 'dashed')

    #plt.show()
    plt.savefig("plot.png")

x_list = []
y_list = []

