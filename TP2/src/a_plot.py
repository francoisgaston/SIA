import pandas as pd
import sys
from plotter import bar_normalize_plot, line_plot


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])

    ans = line_plot(csv, "Variacionde fitness en funcion de variación de A")

    print(ans)

