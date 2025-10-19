from random import randint, uniform, sample, shuffle, random


def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    # Choosing two points for the crossover to occur.
    co_point = randint(1, len(p1) - 2)

    # Executing the crossover.
    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2


def cycle_xo_binary_input(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    # Shuffling the indexes.
    index_list_1 = sample(range(len(p1)), len(p2))
    index_list_2 = sample(range(len(p2)), len(p2))

    # Offspring placeholders.
    offspring1 = [None] * len(p1)
    memory_offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p2)
    memory_offspring2 = [None] * len(p2)

    while None in offspring1:
        index = offspring1.index(None)
        val1 = index_list_1[index]
        val2 = index_list_2[index]

        # Copy the cycle elements.
        while val1 != val2:
            offspring1[index] = p1[index_list_1[index]]
            memory_offspring1[index] = index_list_1[index]
            offspring2[index] = p2[index_list_2[index]]
            memory_offspring2[index] = index_list_2[index]
            val2 = index_list_2[index]
            index = index_list_1.index(val2)

        # Copy the rest.
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index_list_2[index]]
                    memory_offspring1[index] = index_list_2[index]
                    offspring2[index] = p1[index_list_1[index]]
                    memory_offspring2[index] = index_list_1[index]

    offspring1_sorted = [0] * len(p1)
    offspring2_sorted = [0] * len(p2)

    # Reordering the indexes according to their original indexes.
    for index, binary in zip(memory_offspring1, offspring1):
        offspring1_sorted[index] = binary

    for index, binary in zip(memory_offspring2, offspring2):
        offspring2_sorted[index] = binary

    return offspring1_sorted, offspring2_sorted


def pmx_binary_input(p1, p2):
    """Implementation of partially matched crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    # Shuffling the indexes.
    index_list_1 = sample(range(len(p1)), len(p2))
    index_list_2 = sample(range(len(p2)), len(p2))

    # Choosing two random points to be the crossover points.
    xo_points = sample(range(len(p1)), 2)
    xo_points.sort()

    def pmx_offspring(x, y, index_list_x, index_list_y):

        # Starting the placeholders.
        o_binary = [None] * len(x)
        o_cardinal = [None] * len(x)

        # Filling the middle units with the indexes.
        o_cardinal[xo_points[0]:xo_points[1]] = index_list_x[xo_points[0]:xo_points[1]]
        # Using the filled middle index to fill the binary offspring.
        o_binary[xo_points[0]:xo_points[1]] = [x[i] for i in o_cardinal[xo_points[0]:xo_points[1]]]

        # Finding the values in the segment of "index_list_y" that are not in "index_list_x".
        z = set(index_list_y[xo_points[0]:xo_points[1]]) - set(index_list_x[xo_points[0]:xo_points[1]])

        # For the numbers that exist in the segment:
        for i in z:
            temp = i
            index = index_list_y.index(index_list_x[index_list_y.index(temp)])
            if o_cardinal[index] is None:
                o_cardinal[index] = i
                o_binary[index] = y[i]
            else:
                while o_cardinal[index] is not None:
                    temp = index
                    index = index_list_y.index(index_list_x[temp])
                o_cardinal[index] = i
                o_binary[index] = x[i]

        # For the numbers that doesn't exist in the segment:
        while None in o_cardinal:
            index = o_cardinal.index(None)
            o_cardinal[index] = index_list_y[index]
            o_binary[index] = y[o_cardinal[index]]

        # Reordering the indexes according to their original indexes.
        sorted_binary_list = [0] * len(x)
        for index, binary in zip(o_cardinal, o_binary):
            sorted_binary_list[index] = binary

        return sorted_binary_list

    offspring1, offspring2 = pmx_offspring(p1, p2, index_list_1, index_list_2), pmx_offspring(p2, p1, index_list_2,
                                                                                              index_list_1)
    return offspring1, offspring2


def uniform_crossover(p1, p2):
    """Implementation of uniform crossover for binary representations.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    # Starting the placeholders.
    offspring1 = []
    offspring2 = []
    for i in range(len(p1)):

        # Deciding to each offspring that specific index goes.
        if random() < 0.5:
            offspring1.append(p1[i])
            offspring2.append(p2[i])
        else:
            offspring1.append(p2[i])
            offspring2.append(p1[i])

    return offspring1, offspring2
