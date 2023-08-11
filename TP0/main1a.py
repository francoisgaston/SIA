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

