import json
import csv
import sys
from datetime import datetime
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

import plotly.graph_objects as go
import numpy as np

def plot_bar_diagram(pokemons, values, filename):

    fig = go.Figure()

    for pokemon, pokeballs_avg in avg_per_pokemon:
        name, value = pokeballs_avg
        values[name].append(value)

    fig.add_trace(
        go.Bar(name='ultraball', x=pokemons, y = values["ultraball"]),
    )

    fig.add_trace(
        go.Bar(name='fastball', x=pokemons, y = values["fastball"]),
    )

    fig.add_trace(
        go.Bar(name='heavyball', x=pokemons, y = values["heavyball"])
    )

    fig.show()


def write_to_csv(filename, data):
    with open(filename, 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the config file as an argument.")
        sys.exit(1)
    
    factory = PokemonFactory("pokemon.json")

    pokemons = []
    
    values = {
                "ultraball": [], "fastball": [], "heavyball": []
            }

    with open(f"{sys.argv[1]}", "r") as f:
        config = json.load(f)
        avg_per_pokemon = []

        for _pokemon in config["pokemons"]:
            
            pokemons.append(_pokemon)
            

            pokemon = factory.create(_pokemon, config["level"], getattr(StatusEffect, config["status_effect"]), config["current_hp"])

            effectiveness_base_pokeball = 0
            for i in range(config["times"]):
                i, capture_rate = attempt_catch(pokemon, config["base_pokeball"], config["noise"])
                if i == True:
                    effectiveness_base_pokeball += 1
            effectiveness_base_pokeball /= config["times"]

            effectiveness_per_ball = []

            for _ball in config["pokeballs"]:
                avg = 0
                for i in range(config["times"]):
                    i, capture_rate = attempt_catch(pokemon, _ball, config["noise"])
                    if i == True:
                        avg += 1
                avg /= config["times"]
                values[_ball].append(avg / effectiveness_base_pokeball)

        

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        CSV = config["output"] + "_" + timestamp + ".csv"
        write_to_csv(CSV, values)
        print(values)
    
    filename = "graphs/pokeball_effectiveness_per_pokemon.html"
    plot_bar_diagram(pokemons, values, filename)
            

            




