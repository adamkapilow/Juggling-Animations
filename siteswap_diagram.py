import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def throw_func(throw, catch):
    return lambda x : -(x - throw)*(x - catch)*(1/(catch - throw))

def make_plot(throw_heights, colors=None, cycles=3):
    plot, axes = plt.subplots()
    axes.set_yticks([])
    axes.tick_params(labelsize=20)
    N = len(throw_heights)
    start = -cycles*N
    end = cycles*N + 1
    tick_locations = np.arange(start, end, 1)
    tick_labels = []
    for i in range(start, end):
        tick_labels.append(str(throw_heights[i % N]))
    axes.set_xticks(tick_locations)
    axes.set_xticklabels(tick_labels)
    
    for i in range(start, end):
        if throw_heights[i % N] == 0:
            pass
        catch = i + throw_heights[i % N]
        x = np.linspace(i, catch, 50*np.abs(catch - i))
        y = np.apply_along_axis(throw_func(x[0], x[-1]), 0, x)
        if colors == None:
            color = 'r'
        else:
            color = colors[i % len(colors)]
        plt.plot(x, y, color)
    plt.show()

make_plot([5,3,1], colors=['r','k','b','b','k','r'], cycles=4)