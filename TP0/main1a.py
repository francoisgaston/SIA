import json
import csv
import sys
from datetime import datetime
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect
import plotly.graph_objects as go

import numpy as np

def plot_bar_diagram(catch_attempts, filename):
    pokeballs = {}
    
    for _, ball, prob in catch_attempts:
        if ball not in pokeballs:
            pokeballs[ball] = []
        pokeballs[ball].append(prob)

    x_values = []
    y_values = []
    lower_errors = []
    upper_errors = []

    for ball, probs in pokeballs.items():
        x_values.append(ball)
        mean_effectiveness = np.mean(probs)
        y_values.append(mean_effectiveness)
        lower_error = mean_effectiveness - min(probs)
        upper_error = max(probs) - mean_effectiveness
        lower_errors.append(lower_error)
        upper_errors.append(upper_error)

    # Create the bar chart using Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        error_y=dict(type='data', symmetric=False, array=upper_errors, arrayminus=lower_errors),
        name='Efectividad',
    ))

    fig.update_layout(
        title='Efectividad de Diferentes Pokeballs en Capturar Pokémon',
        xaxis_title='Pokeballs',
        yaxis_title='Efectividad',
        barmode='group'
    )

    # Save the figure to HTML
    fig.write_html(filename)
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
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    with open(f"{sys.argv[1]}", "r") as f:
        config = json.load(f)
        CSV = config["output"] + "_" + timestamp + ".csv"
        catch_attempts = []
        
        for pok in config["pokemons"]:
            pokemon = factory.create(pok, config["level"], getattr(StatusEffect, config["status_effect"]), config["current_hp"])
            
            for ball in config["pokeballs"]:
                average_prob = 0
                for _ in range(config["times"]): 
                    _, capture_rate = attempt_catch(pokemon, ball, config["noise"])
                    average_prob += capture_rate
                average_prob /= config["times"]
                catch_attempts.append((pok, ball, average_prob))
        
        write_to_csv(CSV, catch_attempts)

filename = "graphs/pokemon_effectiveness.html"
plot_bar_diagram(catch_attempts, filename)

