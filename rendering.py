import matplotlib.pyplot as plt
# Stats library
import numpy as np

def get_colors(amount):
    return [plt.cm.get_cmap("Spectral")(each) for each in np.linspace(0, 1, len(amount))]

def render_scatter_plot(x, y, ymin, ymax, title, savefig):
    plt.scatter(x, y)
    plt.ylim(ymin, ymax)
    plt.title(title)
    plt.savefig(savefig)
    plt.close()
