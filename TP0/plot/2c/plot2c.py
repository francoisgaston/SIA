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
# The catch rate is rounded to the number of decimals places specified in the config file
def get_catch_rate_per_pokemon_and_level(data, pokemons, decimals_places):
    catch_rate_per_pokemon_and_level = {}
    for row in data:
        pokemon_name = row[0]
        if pokemon_name not in pokemons:
            continue
        level = int(row[1])
        catch_rate = float("{:.{}f}".format(float(row[2]), decimals_places))
        if pokemon_name not in catch_rate_per_pokemon_and_level:
            catch_rate_per_pokemon_and_level[pokemon_name] = {}
        if level not in catch_rate_per_pokemon_and_level[pokemon_name]:
            catch_rate_per_pokemon_and_level[pokemon_name][level] = []
        catch_rate_per_pokemon_and_level[pokemon_name][level].append(catch_rate)
    return catch_rate_per_pokemon_and_level


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
def calculate_catch_rate_data_per_pokemon_and_level(catch_rate_per_pokemon_and_level):
    catch_rate_data_per_pokemon_and_level = {}
    for pokemon_name in catch_rate_per_pokemon_and_level:
        catch_rate_data_per_pokemon_and_level[pokemon_name] = {}
        for level in catch_rate_per_pokemon_and_level[pokemon_name]:
            data = {}
            data["average"] = sum(catch_rate_per_pokemon_and_level[pokemon_name][level]) / len(
                catch_rate_per_pokemon_and_level[pokemon_name][level])
            data["min"] = data["average"] - min(catch_rate_per_pokemon_and_level[pokemon_name][level])
            data["max"] = max(catch_rate_per_pokemon_and_level[pokemon_name][level]) - data["average"]
            catch_rate_data_per_pokemon_and_level[pokemon_name][level] = data
    return catch_rate_data_per_pokemon_and_level


# Creates a graph with the data where:
# - The x axis is the level
# - The y axis is the catch rate
# - Each pokemon is a line in the graph
# - The error bars are the min and max values
# - The title, xaxis_title and yaxis_title are taken from the config file
# - The graph is saved to a HTML file with the name specified in the config file
def graph(catch_rate_data_per_pokemon_and_level, graph_data, filename):
    fig = go.Figure()
    for pokemon_name in catch_rate_data_per_pokemon_and_level:
        x = []
        y = []
        max = []
        min = []
        for level in catch_rate_data_per_pokemon_and_level[pokemon_name]:
            x.append(level)
            y.append(catch_rate_data_per_pokemon_and_level[pokemon_name][level]["average"])
            max.append(catch_rate_data_per_pokemon_and_level[pokemon_name][level]["max"])
            min.append(catch_rate_data_per_pokemon_and_level[pokemon_name][level]["min"])
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                name=pokemon_name.capitalize(),
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
    catch_rate_per_pokemon_and_level = (
        get_catch_rate_per_pokemon_and_level(data, config["pokemons"], config["decimals_places"])
    )
    catch_rate_data_per_pokemon_and_level = (
        calculate_catch_rate_data_per_pokemon_and_level(catch_rate_per_pokemon_and_level)
    )
    graph(catch_rate_data_per_pokemon_and_level, config["graph"], config["output"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the data file as an argument.")
        sys.exit(1)

    with open(f"{sys.argv[1]}", "r") as datafile, open(f"plot/2c/config.json", "r") as configfile:
        data = csv.reader(datafile)
        config = json.load(configfile)
        main(data, config)
