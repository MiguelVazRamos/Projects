from random import uniform, choice, sample, choices
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    # Finding the worse fitness out of the population.
    lowest_fitness = 100
    for i in population:
        if i.fitness[0] <= lowest_fitness:
            lowest_fitness = i.fitness[0]

    # We want to sum the absolute value of the lowest fitness to every observation,
    # as we don't want to risk that the total_fitness of our population is 0 and then
    # bug the uniform(0, total_fitness) function.
    absolute_fitness = 0
    if lowest_fitness < 0:
        absolute_fitness = -lowest_fitness

    if population.optim == "max":

        # Sum total fitness.
        total_fitness = sum([(i.fitness[0] + absolute_fitness) for i in population])
        # Get a 'position' on the wheel.
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin.
        for individual in population:
            position += (individual.fitness[0] + absolute_fitness)
            if position > spin:
                return individual

    elif population.optim == "min":

        # Finding the maximum of each fitness plus the absolute fitness.
        max_joint_fitness = max([(i.fitness[0] + absolute_fitness) for i in population])

        # Obtaining the total fitness taking into consideration that this is a minimization problem.
        total_fitness = sum([(max_joint_fitness - (i.fitness[0] + absolute_fitness))/(max_joint_fitness + 0.0001) for i
                             in population])
        # Get a "position" on the wheel.
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin.
        for individual in population:
            position += ((max_joint_fitness - (individual.fitness[0] + absolute_fitness)) / (max_joint_fitness + 0.0001))
            if position > spin:
                return individual

    else:
        raise Exception("No optimization specified (min or max).")


def tournament_sel(population, size=4):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: The best individual in the tournament.
    """

    # Select individuals based on tournament size
    # with choice, there is a possibility of repetition in the choices,
    # so every individual has a chance of getting selected
    tournament = [choice(population.individuals) for _ in range(size)]

    # with sample, there is no repetition of choices
    # tournament = sample(population.individuals, size)
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    if population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))


def rank(population):
    # Ranking individuals based on optimality approach.
    if population.optim == 'max':
        population.individuals.sort(key=attrgetter('fitness'))
    elif population.optim == 'min':
        population.individuals.sort(key=attrgetter('fitness'), reverse=True)

    # Summing all rankings.
    total = sum(range(population.size+1))
    # Getting random positions.
    spin = uniform(0, total)
    position = 0
    # Iterating until spin is found.
    for count, individual in enumerate(population):
        position += count + 1
        if position > spin:
            return individual
