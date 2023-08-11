import json
import csv
import sys
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
    catch_attempts = []
    with open(f"{sys.argv[1]}", "r") as f:
        config = json.load(f)
        ball = config["pokeball"]
        CSV = config["output_csv"]
        pokemon = factory.create(config["pokemon"], 100, StatusEffect.NONE, 1)

        catch_attempts.append(("No noise: ", attempt_catch(pokemon, ball)))
        print("No noise: ", attempt_catch(pokemon, ball))
        for _ in range(10):
            catch_attempts.append(("Noisy: ", attempt_catch(pokemon, ball, 0.15)))
            print("Noisy: ", attempt_catch(pokemon, ball, 0.15))

        write_to_csv(CSV, catch_attempts)
        print(f"Results written to {CSV}")
