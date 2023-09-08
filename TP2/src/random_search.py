import json
from main import run_genetic 
import random
from datetime import datetime, timedelta

def evaluate_model(config):
    """
    Evaluate the performance of the Genetic Algorithm based on the given configuration.

    Parameters:
        config (dict): A dictionary containing the configuration settings for the Genetic Algorithm.

    Returns:
        dict: A dictionary containing performance metrics such as mean_fitness, max_fitness, and min_fitness.
    """
    ans = run_genetic(
        individual_class=config["class"],
        crossover=config["crossover"],
        population_0_count=config["population_0_count"],
        selection_1=config["selection_1"],
        selection_2=config["selection_2"],
        replace_1=config["replace_1"],
        replace_2=config["replace_2"],
        replace=config["replace"],
        mutation=config["mutation"],
        mutation_probability=config["mutation_probability"],
        stop_condition=config["stop_condition"],
        stop_condition_options=config["stop_condition_options"],
        K=config["K"],
        A=config["A"],
        B=config["B"],
        last_generation_count=config["population_0_count"]
    )

    # Extract the last value (fitness) of each tuple
    fitness_values = [x[-1] for x in ans]
    
    # Calculate the summary statistics
    mean_fitness = sum(fitness_values) / len(fitness_values) if len(fitness_values) > 0 else 0

    return mean_fitness
    

# Default configuration template
config_template = {
    "output": "src/results/out",
    "population_0_count": 100,
    "stop_condition": "CHECK_CONTENT",
    "stop_condition_options": {
        "max_generations": 1000,
        "max_time": 5,
        "acceptable_solution": 1,
        "limit_generations": 10
    },
    "class": "WARRIOR",
    "A": 0.8,
    "B": 0.5,
    "K": 28,
    "selection_1": {
        "name": "ROULETTE",
        "m": 5
    },
    "selection_2": {
        "name": "UNIVERSAL",
        "tc": 10,
        "t0": 50,
        "c": 1
    },
    "repeat_in_selection": True,
    "crossover": "ANULAR",
    "mutation": "MULTI_GEN_UNIFORM",
    "mutation_probability": 1,
    "deter_tournament": {
        "m": 5
    },
    "replace": "SESGO",
    "replace_1": {
        "name": "ELITE",
        "m": 5
    },
    "replace_2": {
        "name": "BOLTZMANN",
        "tc": 10,
        "t0": 50,
        "c": 1
    }
}

# Parameter space for random search
param_space = {
    "population_0_count": [50, 100, 150, 200],
    "stop_condition": ["MAX_GENERATIONS", "MAX_TIME", "ACCEPTABLE_SOLUTION", "CHECK_CONTENT"],
    "class": ["WARRIOR"],
    "A": [0.1, 0.5, 0.8],
    "B": [0.1, 0.3, 0.5],
    "K": [16, 28, 40],
    "repeat_in_selection": [True, False],
    "crossover": ["SINGLE_POINT", "TWO_POINT", "UNIFORM_POINT", "ANULAR"],
    "mutation": ["GEN_UNIFORM", "GEN_NON_UNIFORM", "MULTI_GEN_UNIFORM", "MULTI_GEN_NON_UNIFORM"],
    "mutation_probability": [0.5, 1, 0.9, 0.2],
    "replace": ["TRADICIONAL", "SESGO"],
    "selection_1": {
        "name": ["ROULETTE", "UNIVERSAL", "ELITE"],
        "m": [3, 5, 7]
    },
    "selection_2": {
        "name": ["ROULETTE", "UNIVERSAL", "ELITE"],
        "tc": [5, 10],
        "t0": [25, 50],
        "c": [0.5, 1]
    },
    "deter_tournament": {
        "m": [3, 5, 7]
    },
    "replace_1": {
        "name": ["ELITE"],
        "m": [3, 5, 7]
    },
    "replace_2": {
        "name": ["BOLTZMANN"],
        "tc": [5, 10],
        "t0": [25, 50],
        "c": [0.5, 1]
    }
}

# Initialize search
max_evals = 20
start_time = datetime.now()
best_config = None
best_performance = float('-inf')

# Random search loop
for eval_num in range(max_evals):
    # Generate a random configuration
    current_config = {}
    for param, possible_values in param_space.items():
        if isinstance(possible_values, list):
            current_config[param] = random.choice(possible_values)
        elif isinstance(possible_values, dict):
            current_config[param] = {}
            for sub_param, sub_possible_values in possible_values.items():
                current_config[param][sub_param] = random.choice(sub_possible_values)

    # Merge with template
    merged_config = {**config_template, **current_config}

    # Evaluate the current configuration
    current_performance = evaluate_model(merged_config)

    # Update the best configuration
    if current_performance > best_performance:
        best_performance = current_performance
        best_config = merged_config

    # Stop condition based on time
    if datetime.now() - start_time > timedelta(minutes=10):
        break

# Output the best configuration
print(f"Best performance: {best_performance}")
print(f"Best configuration: {json.dumps(best_config, indent=4)}")

