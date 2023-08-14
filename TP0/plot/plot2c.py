import sys
import csv
import json
import plotly.graph_objects as go


# Creates a data structure like this:
# {
#     "bulbasaur": {
#         1: [0.2, 0.1, 0.3, 0.8, 0.5],
#         2: [0.3, 0.6, 0.5, 0.7, 0.5],
#         3: [0.1, 0.6, 0.9, 0.8, 0.5],
#         ...
#     },
#     ...
# }
# Only consider the pokemons in the config file
def get_effectiveness_per_pokemon_and_level(data, pokemons):
    effectiveness_per_pokemon_and_level = {}
    for row in data:
        pokemon_name = row[0]
        if pokemon_name not in pokemons:
            continue
        level = int(row[1])
        effectiveness = float(row[2])
        if pokemon_name not in effectiveness_per_pokemon_and_level:
            effectiveness_per_pokemon_and_level[pokemon_name] = {}
        if level not in effectiveness_per_pokemon_and_level[pokemon_name]:
            effectiveness_per_pokemon_and_level[pokemon_name][level] = []
        effectiveness_per_pokemon_and_level[pokemon_name][level].append(effectiveness)
    return effectiveness_per_pokemon_and_level


# Creates a data structure like this:
# {
#     "bulbasaur": {
#         1: {
#             "average": 0.5,
#             "min": 0.1,
#             "max": 0.4
#         },
#         2: {
#             "average": 0.6,
#             "min": 0.1,
#             "max": 0.5
#         },
#         ...
#     },
#     ...
# }
def calculate_effectiveness_data_per_pokemon_and_level(effectiveness_per_pokemon_and_level):
    effectiveness_data_per_pokemon_and_level = {}
    for pokemon_name in effectiveness_per_pokemon_and_level:
        effectiveness_data_per_pokemon_and_level[pokemon_name] = {}
        for level in effectiveness_per_pokemon_and_level[pokemon_name]:
            data = {}
            data["average"] = sum(effectiveness_per_pokemon_and_level[pokemon_name][level]) / len(
                effectiveness_per_pokemon_and_level[pokemon_name][level])
            data["min"] = min(effectiveness_per_pokemon_and_level[pokemon_name][level])
            data["max"] = max(effectiveness_per_pokemon_and_level[pokemon_name][level])
            effectiveness_data_per_pokemon_and_level[pokemon_name][level] = data
    return effectiveness_data_per_pokemon_and_level


# Creates a graph with the data where:
# - The x axis is the level
# - The y axis is the catch rate
# - Each pokemon is a line in the graph
# - The error bars are the min and max values
# - The title, xaxis_title and yaxis_title are taken from the config file
# - The graph is saved to a HTML file with the name specified in the config file
def graph(effectiveness_data_per_pokemon_and_level, graph_data, filename):
    decimal_places = graph_data["decimal_places"]
    fig = go.Figure()
    for pokemon_name in effectiveness_data_per_pokemon_and_level:
        x = []
        y = []
        max = []
        min = []
        for level in effectiveness_data_per_pokemon_and_level[pokemon_name]:
            data = effectiveness_data_per_pokemon_and_level[pokemon_name][level]
            x.append(level)
            y.append(data["average"])
            max.append(data["max"] - data["average"])
            min.append(data["average"] - data["min"])
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                name=pokemon_name.capitalize(),
                hovertemplate=graph_data["xaxis_title"] + ": %{x}<br>" +
                              graph_data["yaxis_title"] + ": %{y:." + str(decimal_places) +
                              "f} (+%{error_y.array:." + str(decimal_places) +
                              "f} / -%{error_y.arrayminus:." + str(decimal_places) +
                              "f})<extra></extra>",
                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=max,
                    arrayminus=min
                )
            )
        )
    fig.update_layout(
        title=graph_data["title"],
        xaxis_title=graph_data["xaxis_title"],
        yaxis_title=graph_data["yaxis_title"],
    )
    fig.write_html(filename + ".html")
    fig.show()


def main(data, config):
    effectiveness_per_pokemon_and_level = (
        get_effectiveness_per_pokemon_and_level(data, config["pokemons"])
    )
    effectiveness_data_per_pokemon_and_level = (
        calculate_effectiveness_data_per_pokemon_and_level(effectiveness_per_pokemon_and_level)
    )
    graph(effectiveness_data_per_pokemon_and_level, config["graph"], config["output"])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide the data file and the config file as arguments.")
        sys.exit(1)

    with open(f"{sys.argv[1]}", "r") as datafile, open(f"{sys.argv[2]}", "r") as configfile:
        data = csv.reader(datafile)
        config = json.load(configfile)
        main(data, config)
