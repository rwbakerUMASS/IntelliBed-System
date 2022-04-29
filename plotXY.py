from matplotlib import pyplot as plt
import numpy as np

def plot(x,y):
    plt.scatter(x,y)
    plt.title("Center of Mass")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.pause(0.01)