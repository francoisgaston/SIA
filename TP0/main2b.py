import json
import csv
import sys
import numpy as np
from datetime import datetime
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the config file as an argument.")
        sys.exit(1)

    factory = PokemonFactory("pokemon.json")
    timestamp = datetime.now().strftime("%m%d%H%M")
    catch_attempts = []

    with open(f"{sys.argv[1]}", "r") as f:
        config = json.load(f)
        ball = config["pokeball"]
        CSV = "./data/2b/" + config["output"] + "_" + timestamp + ".csv"
        times = config["times"]
        noise = config["noise"]
        dots = config["dots"]
        inter = 1/dots

        # Plantear el problema de lento vs memoria usada
        with open(CSV, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "current_hp", "capture_rate"])

            for pokemon_config in config["pokemons"]:
                for hp in np.arange(0, 1, inter):
                    hp = round(hp, 2)

                    pokemon = factory.create(pokemon_config["name"], pokemon_config["level"], getattr(StatusEffect, pokemon_config["status_effect"]), hp)

                    for _ in range(config["times"]):
                        writer.writerow([pokemon.name, hp, attempt_catch(pokemon, ball, noise)[1]])
