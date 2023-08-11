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
    catch_attempts = []
    with open(f"{sys.argv[1]}", "r") as f:
        config = json.load(f)
        ball = config["pokeball"]
        CSV = config["output"] + "_" + timestamp + ".csv"
        pokemon = factory.create(config["pokemon"]["name"], config["pokemon"]["level"], getattr(StatusEffect,config["pokemon"]["status_effect"]) ,config["pokemon"]["current_hp"])
        for _ in range(config["times"]):
            catch_attempts.append(attempt_catch(pokemon, ball, config["noise"]))

        write_to_csv(CSV, catch_attempts)
