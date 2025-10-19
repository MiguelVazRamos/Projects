from charles import Population, Individual
from random import choices
import random
from copy import deepcopy
from crossover import cycle_xo_binary_input, pmx_binary_input, single_point_co, uniform_crossover
from mutation import swap_mutation, inversion_mutation, binary_mutation
from selection import tournament_sel, fps, rank
import numpy as np

# It is here that we choose which difficulty we are going to tackle. We can only have one of them
# turned on. If we want to tackle the private hospital setting we use data_easy sheet, and if we want
# to tackle the public hospital setting we use the data_hard sheet.

# from data_easy import days, shifts, workers, workers_per_shift, holidays, skilled_shifts, skills, preferences
from data_medium_hard import days, shifts, workers, workers_per_shift, holidays, skilled_shifts, skills, preferences


# Creating the function that will create our base representation.
def get_representation(self):
    # Calculating the total number of indexes.
    total_indexes = days * shifts * workers
    # Representation placeholder.
    representation = [0] * total_indexes
    # Calculating the total number of shifts.
    total_shifts = days * shifts

    # Calculating the total number of workers needed overall across all the shifts.
    total_workers_shifts = sum(workers_per_shift)

    # Calculating the ideal number of shifts that each worker should work.
    perfect_shifts_per_worker = int(total_workers_shifts / workers)

    # Placeholder to know how many workers were already placed.
    placed = 0

    # Iterating through all the workers.
    for worker in range(workers):
        # Choosing which are the shifts that this worker will work.
        positions = random.sample(range(total_shifts * worker, total_shifts * (worker + 1)), perfect_shifts_per_worker)

        # Placing the bips on the representation.
        for pos in positions:
            representation[pos] = 1
            placed += 1

    # We attribute randomly the shifts that are left.
    while placed != total_workers_shifts:
        random_position = random.randint(0, total_indexes - 1)
        if representation[random_position] == 0:
            representation[random_position] = 1
            placed += 1

    return representation


Individual.get_representation = get_representation


def get_fitness(self):
    # Initiating the placeholders for the variable we are going to work with on the function.
    fitness = 0
    total_shifts = shifts * days
    distributed_workers = 0
    consecutive_shifts = 0
    shifts_2_days = 0
    shifts_wrong_filled = 0
    holidays_not_met = 0
    skilled_shifts_failed = 0
    preferences_met = 0
    preferences_not_met = 0

    # Checking if the distribution of workers across the shifts is well-balanced.
    for i in range(workers):
        calendar = self.representation[(i * total_shifts):((i + 1) * total_shifts)]
        working_days = sum(calendar)
        if (working_days >= (4 * (days / 7))) and (working_days <= (6 * (days / 7))):
            fitness += 1000  # We increase 1000 of fitness for each worker that has its shifts well-distributed.
            distributed_workers += 1

    # Checking if any worker works two shifts in a row.
    for i in range(workers):
        for j in range(total_shifts - 1):
            calendar = self.representation[(i * total_shifts):((i + 1) * total_shifts)]
            if calendar[j] == calendar[j + 1] == 1:
                fitness -= 100  # Decrease 100 of fitness for each consecutive working shift.
                consecutive_shifts += 1

    # Checking if any worker works more than 3 shifts in 2 consecutive days.
    for i in range(workers):
        calendar = self.representation[(i * total_shifts):((i + 1) * total_shifts)]
        for j in range(days):
            two_day_span = calendar[(2 * j * shifts):(2 * (j + 1) * shifts)]
            if sum(two_day_span) > 3:
                fitness -= 100  # Fitness decreases 100 if any worker works more than 3 shifts in 2 days.
                shifts_2_days += 1

    # Checking if the number of workers per shift was met.
    for shift in range(total_shifts):
        number_of_workers = 0
        for worker in range(workers):
            index = shift + worker * total_shifts
            number_of_workers += self.representation[index]
        if number_of_workers != workers_per_shift[shift]:
            fitness -= 300  # For each number of workers on a shift that is not met, fitness decreases by 300.
            shifts_wrong_filled += 1

    # Checking if the holidays of each worker were met.
    for i in range(workers):
        calendar = self.representation[(i * total_shifts):((i + 1) * total_shifts)]
        for j in range(total_shifts):
            if holidays[i][j] == 1 and calendar[j] == 1:
                fitness -= 100  # If the worker is scheduled to work on a day of holidays fitness decreases by 100.
                holidays_not_met += 1

    # Checking if the current allocation has the skilled workers assigned to the skilled shifts.
    for i in range(workers):
        calendar = self.representation[(i * total_shifts):((i + 1) * total_shifts)]
        for shift, required_skills in skilled_shifts.items():
            if calendar[shift] == 1:
                missing_skill = False  # Introducing a boolean flag, as we don't want to subtract 5 multiple times.
                for skill in required_skills:
                    if skill not in skills[i]:
                        missing_skill = True
                        break
                if missing_skill:
                    fitness -= 200  # If the worker doesn't present the required skill fitness decreases by 200.
                    skilled_shifts_failed += 1

    # Checking if the preferences of each worker were met.
    for i in range(workers):
        calendar = self.representation[(i * total_shifts):((i + 1) * total_shifts)]
        for j in range(total_shifts):

            if (preferences[i][j] == 1 and calendar[j] == 1) or (preferences[i][j] == -1 and calendar[j] == 0):
                fitness += 10  # For each preference of a worker that is met, fitness increases by 10.
                preferences_met += 1

            elif (preferences[i][j] == -1 and calendar[j] == 1) or (preferences[i][j] == 1 and calendar[j] == 0):
                fitness -= 10  # For each preference that is not met, fitness decreases by 10.
                preferences_not_met += 1

    return round(fitness, 2), distributed_workers, consecutive_shifts, shifts_2_days, shifts_wrong_filled,\
        holidays_not_met, skilled_shifts_failed, preferences_met, preferences_not_met


Individual.get_fitness = get_fitness

pop = Population(
    size=100,
    optim="max")

pop.evolve(gens=200, select=rank, mutate=swap_mutation, crossover=uniform_crossover,
           mut_prob=1.00, xo_prob=1.00, elitism=True)
