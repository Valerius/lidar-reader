import matplotlib.pyplot as plt
# Stats library
import numpy as np

def get_colors(amount):
    return [plt.cm.get_cmap("Spectral")(each) for each in np.linspace(0, 1, len(amount))]

