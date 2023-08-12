import json
import csv
import sys
from datetime import datetime
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect
from matplotlib import pyplot as plt
import numpy as np

def plot_bar_diagram(catch_attempts, filename):
    pokeballs = []
    effectiveness = []
    errors = []  
    for _, ball, prob in catch_attempts:
        if ball not in pokeballs:
            pokeballs.append(ball)
            effectiveness.append(prob)
            errors.append(prob * 0.05)

    _, ax = plt.subplots(figsize=(10, 6))

    # Create a bar chart
    y_pos = np.arange(len(pokeballs))
    ax.bar(y_pos, effectiveness, yerr=errors, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_xticks(y_pos)
    ax.set_xticklabels(pokeballs)
    ax.set_xlabel('Pokeballs ')
    ax.set_title('Efectividad en Capturar Pokémon')
    ax.yaxis.grid(True)

    plt.ylabel('Efectividad')
    plt.xticks(rotation=45)

    ax.set_ylabel('Efectividad')
    ax.set_title('Efectividad de Diferentes Pokeballs en Capturar Pokémon')
    ax.set_xticks(y_pos)
    ax.set_xticklabels(pokeballs)

    plt.tight_layout()
    plt.savefig(filename) 
    plt.show()


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

filename = "graphs/pokemon_effectiveness.png"
plot_bar_diagram(catch_attempts, filename)

