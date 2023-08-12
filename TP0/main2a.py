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
        ball = config["pokeball"]
        CSV = "data/2a/"+ config["output"] + "_" + timestamp + ".csv"
        with open(CSV, 'w', newline="") as output:
            writer = csv.writer(output)
            writer.writerow(["pokemon","status_effect","result","current_iter","max_iter"])
            for _pokemon in config["pokemons"]:
                for effect in _pokemon["status_effect"]:
                    pokemon = factory.create(_pokemon["name"], _pokemon["level"],
                                              getattr(StatusEffect, effect), _pokemon["current_hp"])
                    for i in range(config["times"]):
                        res = attempt_catch(pokemon, ball, config["noise"])
                        writer.writerow([pokemon.name, effect, res[0], i+1, config["times"]])
