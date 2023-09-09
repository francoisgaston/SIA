import pandas as pd
import sys
from plotter import bar_normalize_plot, multiple_lines_plot


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])

    ans = multiple_lines_plot(csv, "mutation_probability", "mutation", "mejor fitness para todas las configuraciones de mutación")
    print(ans)
