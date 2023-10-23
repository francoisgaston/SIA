import itertools
import json
import sys
import numpy as np
import pandas as pd
import plotly.express as px


from hopfield import Hopfield


def read_input(file, input_length):
    file1 = open(file, "r+")
    result = [(1 if character == '1' else -1) for character in file1.read().split()]
    result = np.array_split(result, len(result) / input_length)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as config_file:
        config = json.load(config_file)
        input_file = config["input"]
        input_length = config["size"]
        try_file = config["try"]
        combination_size = config["combination_size"]

        patterns = read_input(input_file, input_length)
        letters = {chr(97 + i): patterns[i] for i in range(26)}
        pattern_to_try = read_input(try_file, input_length)
        max_iterations = config["max_iterations"]

        min_avg = []
        for i in range(2, 10):
            combinations = list(itertools.combinations(letters.keys(), i))
            avg_list = []
            for combination in combinations:
                patterns_combination = [np.array(letters[key]) for key in combination]
                max_product, min_product, avg_product = Hopfield._analyse_orthogonality(np.array(patterns_combination))
                avg_list.append((avg_product, combination))
            min_avg.append(min(avg_list))
        df = pd.DataFrame(min_avg, columns=["min", "combination"])
        print(df)
        # fig = px.bar(df, x='', y='min', title='Ortogonalidad minima para cada tamaño de combinaciones')
        #
        # # Show the plot
        # fig.show()
        # Create a bar graph using Plotly
        # fig = px.bar(df, x=df.index, y='min', text='combination', title='Bar Graph with Text Labels')
        #
        # # Update the x-axis labels to match the order
        # fig.update_xaxes(title_text='Order', tickvals=list(range(len(df))), ticktext=df.index + 1)
        #
        # # Show the plot
        # fig.show()
        fig = px.bar(df, x=df.index, y='min', title='Bar Graph with Combination Labels')

        # Customize the x-axis and y-axis
        fig.update_xaxes(title_text='Order', tickvals=list(range(len(df))), ticktext=df['combination'], title_font=dict(size=18))
        fig.update_yaxes(title_text='min |<,>| avg')

        # Show the plot
        fig.show()