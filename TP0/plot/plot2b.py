import seaborn
import pandas
import sys
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pandas.read_csv(sys.argv[1])
    res = seaborn.lineplot(data=csv, x="current_hp", y="capture_rate", hue="name", legend="auto", errorbar=("pi", 90)).set(title='%HP vs CAPTURE RATE')

    plt.legend(title='Pokemon')
    plt.savefig(sys.argv[1].replace('csv', 'png'))
    plt.show()
