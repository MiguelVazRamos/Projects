from charles import Population, Individual
from selection import fps, tournament_sel, rank
from mutation import binary_mutation, swap_mutation, inversion_mutation
from crossover import single_point_co, cycle_xo_binary_input, pmx_binary_input, uniform_crossover
from scheduling_problem import get_representation
import numpy as np
from pathlib import Path

# Understand why do we need this here.
Individual.get_representation = get_representation

# The only difference between the best two combinations was on the mutation
# technique. And so, when fine-tuning the mutation and crossover probability
# we are still going to do it for two different models.
mutation_methods = {"binary_mutation": binary_mutation,
                    "swap_mutation": swap_mutation}

# Jumping 0.20 each time on the probability of crossover and mutation:
mutation_prob = {"0.2": 0.2, "0.4": 0.4, "0.6": 0.6, "0.8": 0.8, "1.0": 1.0}
crossover_prob = {"0.2": 0.2, "0.4": 0.4, "0.6": 0.6, "0.8": 0.8, "1.0": 1.0}

# Creating a dictionary called "store_dict" that will store the results.
storing_dict = {}

# For each mutation method.
for mut_method, mut_function in mutation_methods.items():
    # For each crossover probability.
    for cross_value, cross_prob in crossover_prob.items():
        # For each mutation probability.
        for mutation_value, mut_prob in mutation_prob.items():

            # Create an accumulator.
            fitness_accumulator = np.array([0] * 100, dtype=np.float64)
            # Run 35 times each algorithm.
            for i in range(35):
                # Starting the Population.
                pop = Population(size=100,
                                 optim="max",
                                 filename=
                                 f"/{cross_value}_{mutation_value}_{mut_method}",
                                 folder=Path("hard_parameter_tuning") / "test")

                pop.evolve(gens=100,
                           select=rank,
                           mutate=mut_function,
                           crossover=uniform_crossover,
                           mut_prob=mut_prob,
                           xo_prob=cross_prob,
                           elitism=True,
                           store=True)

                # Summing the values of every fitness for every generation.
                fitness_accumulator += np.array(pop.fitnesses)

            # Doing the average of all the fitnesses.
            average_fitness_per_generation = fitness_accumulator / 35
            storing_dict[cross_value + " / " + mutation_value + " / " + mut_method] = \
                average_fitness_per_generation

print(storing_dict.items())
