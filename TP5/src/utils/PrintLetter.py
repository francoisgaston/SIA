import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize

def plot_pattern(pattern, target_size=(20, 20), filename="plots/pattern.png"):
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.makedirs(path)

    pattern_reshaped = np.array(pattern).reshape(target_size)

    # Set normalization range from 0 to 1
    norm = Normalize(vmin=0, vmax=1)

    # Define a custom colormap with white, greyscale, and black segments
    cmap = LinearSegmentedColormap.from_list('custom_gray', [(1, 1, 1), (0.5, 0.5, 0.5), (0, 0, 0)], N=256)

    plt.imshow(pattern_reshaped, cmap=cmap, norm=norm)
    plt.axis('off')
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    pattern = np.array([0 ,0 ,0 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,1 ,0 ,1 ,0 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,1 ,0 ,1 ,0 ,1 ,0 ,0 ,0 ,1 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,0 ,0])

    plot_pattern(pattern, target_size=(12, 12))
