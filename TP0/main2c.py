import json
import sys
from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect
from src.utils import write_to_csv


def main(config):
    factory = PokemonFactory("pokemon.json")
    catch_attempts = []

    filename_prefix = config["output"]
    times_per_level = config["times_per_level"]
    noise = config["noise"]
    pokeball = config["pokeball"]
    pokemons_names = config["pokemons"]
    current_hp = config["current_hp"]
    status_effect = getattr(StatusEffect, config["status_effect"])

    # For each pokemon, for each level, try to catch it times_per_level times
    for pokemon_name in pokemons_names:
        for level in range(1, 101):
            pokemon = factory.create(pokemon_name, level, status_effect, current_hp)
            for _ in range(times_per_level):
                attempt = attempt_catch(pokemon, pokeball, noise)
                catch_attempts.append(tuple((pokemon_name, level, attempt[1], attempt[0])))

    # Save the results to a csv file
    write_to_csv(
        filename_prefix=filename_prefix,
        data=catch_attempts
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the config file as an argument.")
        sys.exit(1)

    with open(f"{sys.argv[1]}", "r") as f:
        config = json.load(f)
        main(config)
