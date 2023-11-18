import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize

def plot_pattern(pattern, iteration, save_path="plots"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    pattern_reshaped = np.array(pattern).reshape((7, 5))

    # Set normalization range from 0 to 1
    norm = Normalize(vmin=0, vmax=1)

    # Define a custom colormap with white, greyscale, and black segments
    cmap = LinearSegmentedColormap.from_list('custom_gray', [(1, 1, 1), (0.5, 0.5, 0.5), (0, 0, 0)], N=256)

    plt.imshow(pattern_reshaped, cmap=cmap, norm=norm)
    plt.axis('off')
    filename = os.path.join(save_path, f"pattern_{iteration}.png")
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    pattern = np.array([0, 0, 1, 0, 0,
                        0, 0, 0.1, 0, 0,
                        0, 0, 0, 1, 0,
                        0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0])

    plot_pattern(pattern, 0)
