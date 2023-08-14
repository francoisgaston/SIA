import json
import csv
import sys
from datetime import datetime
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

def write_to_csv(filename, data):
    with open(filename, 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the config file as an argument.")
        sys.exit(1)
    
    factory = PokemonFactory("pokemon.json")

    with open(f"{sys.argv[1]}", "r") as f:
        config = json.load(f)
        avg_per_pokemon = []

        for _pokemon in config["pokemons"]:
            
            pokemon = factory.create(_pokemon, config["level"], getattr(StatusEffect, config["status_effect"]), config["current_hp"])
            effectiveness_per_ball = []

            for _ball in config["pokeballs"]:
                effectiveness = 0
                for i in range(config["times"]):
                    i, capture_rate = attempt_catch(pokemon, _ball, config["noise"])
                    effectiveness += capture_rate
                effectiveness /= config["times"]
                effectiveness_per_ball.append((_ball, effectiveness))
            avg_per_pokemon.append((_pokemon, effectiveness_per_ball))
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        CSV = config["output"] + "_" + timestamp + ".csv"
        write_to_csv(CSV, avg_per_pokemon)
        print(avg_per_pokemon)
            

            




