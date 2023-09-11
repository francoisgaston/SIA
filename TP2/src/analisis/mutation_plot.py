
import pandas as pd
import sys
from plotter import bar_normalize_plot


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])

    ans = bar_normalize_plot(csv, "mutation", "MULTI_GEN_UNIFORM", "Mutation Vs Fitness", "Test", "fitness / multi_gen_uniform_fitness")

    print(ans)
