from charles import Population, Individual
from selection import fps, tournament_sel, rank
from mutation import binary_mutation, swap_mutation, inversion_mutation
from crossover import single_point_co, cycle_xo_binary_input, pmx_binary_input, uniform_crossover
from scheduling_problem import get_representation
import numpy as np
from pathlib import Path

# Understand why do we need this here.
Individual.get_representation = get_representation

# Selecting the selection methods for the grid-search:
selection_methods = {"fps": fps, "tournament_sel": tournament_sel, "rank": rank}
# Selecting the mutation methods for the grid-search:
mutation_methods = {"binary_mutation": binary_mutation, "swap_mutation": swap_mutation,
                    "inversion_mutation": inversion_mutation}
# Selecting the crossover methods for the grid-search:
crossover_methods = {"single_point_co": single_point_co, "pmx_binary_input": pmx_binary_input,
                     "uniform_crossover": uniform_crossover}
# Selecting some random probabilities for the mutation and crossover (later they will enter grid-search too):
mutation_prob = 0.15
crossover_prob = 0.85

# Creating a dictionary called "store_dict" that will store the results.
storing_dict = {}

# For each selection method.
for sel_method, sel_function in selection_methods.items():
    # For each mutation method.
    for mut_method, mut_function in mutation_methods.items():
        # For each crossover method.
        for cross_method, cross_function in crossover_methods.items():
            # Create an accumulator.
            fitness_accumulator = np.array([0] * 100, dtype=np.float64)
            # Run 35 times each algorithm.
            for i in range(35):
                # Starting the Population.
                pop = Population(size=100,
                                 optim="max",
                                 filename=f"/{cross_method}_{mut_method}_{sel_method}",
                                 folder=Path("hard_first_grid_search") / "test")

                pop.evolve(gens=100,
                           select=sel_function,
                           mutate=mut_function,
                           crossover=cross_function,
                           mut_prob=mutation_prob,
                           xo_prob=crossover_prob,
                           elitism=True,
                           store=True)

                # Summing the values of every fitness for every generation.
                fitness_accumulator += np.array(pop.fitnesses)

            # Doing the average of all the fitnesses.
            average_fitness_per_generation = fitness_accumulator / 35
            storing_dict[sel_method + " / " + mut_method + " / " + cross_method] = average_fitness_per_generation

print(storing_dict.items())
