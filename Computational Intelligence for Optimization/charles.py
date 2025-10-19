from random import shuffle, choice, sample, random, choices
from operator import attrgetter
from copy import deepcopy
from pathlib import Path
import csv


class Individual:
    def __init__(
            self,
            representation=None
    ):
        if representation is None:
            self.representation = self.get_representation()
        else:
            self.representation = representation
        self.fitness = self.get_fitness()

    def get_representation(self):
        raise Exception("You need to monkey path the representation path.")

    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness path.")

    def get_neighbours(self, func, **kwargs):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f'{self.representation}'


class Population:
    def __init__(self, size, optim, filename=None, folder=None):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.gen = 1
        self.fitnesses = []
        self.filename = filename
        self.folder = folder

        for _ in range(size):
            self.individuals.append(
                Individual()
            )

    def evolve(self, gens, xo_prob, mut_prob, select, mutate, crossover, elitism, store=False):

        for i in range(gens):
            new_pop = []

            if elitism:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)

                if random() < xo_prob:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                if random() < mut_prob:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                if self.optim == "max":
                    worst = min(new_pop, key=attrgetter("fitness"))
                    if elite.fitness[0] > worst.fitness[0]:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

                elif self.optim == "min":
                    worst = max(new_pop, key=attrgetter("fitness"))
                    if elite.fitness[0] < worst.fitness[0]:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

            self.individuals = new_pop

            if self.optim == "max":
                best_individual = max(self, key=attrgetter("fitness"))
                print(f'------------------- Generation {self.gen} -------------------\n'
                      f'Best Individual: {best_individual}\n'
                      f'Fitness: {best_individual.fitness[0]}\n'
                      f'Distributed Workers: {best_individual.fitness[1]}\n'
                      f'Consecutive Shifts: {best_individual.fitness[2]}\n'
                      f'Shifts in 2 Days: {best_individual.fitness[3]}\n'
                      f'Shifts Not Completely Filled: {best_individual.fitness[4]}\n'
                      f'Holidays Not Respected: {best_individual.fitness[5]}\n'
                      f'Number of Failed Skilled Shifts: {best_individual.fitness[6]}\n'
                      f'Number of Preferences Respected: {best_individual.fitness[7]}\n'
                      f'Number of Preferences Not Respected: {best_individual.fitness[8]}\n')

                # Adding the best fitness of each generation to the property fitnesses as this will be useful for
                # grid-search and on choosing the best method.
                self.fitnesses.append(best_individual.fitness[0])

            elif self.optim == "min":
                worst_individual = min(self, key=attrgetter("fitness"))
                print(f'------------------- Generation {self.gen} -------------------\n'
                      f'Worst Individual: {worst_individual}\n'
                      f'Fitness: {worst_individual.fitness[0]}\n'
                      f'Distributed Workers: {worst_individual.fitness[1]}\n'
                      f'Consecutive Shifts: {worst_individual.fitness[2]}\n'
                      f'Shifts in 2 Days: {worst_individual.fitness[3]}\n'
                      f'Shifts Not Completely Filled: {worst_individual.fitness[4]}\n'
                      f'Holidays Not Respected: {worst_individual.fitness[5]}\n'
                      f'Number of Failed Skilled Shifts: {worst_individual.fitness[6]}\n'
                      f'Number of Preferences Respected: {worst_individual.fitness[7]}\n'
                      f'Number of Preferences Not Respected: {worst_individual.fitness[8]}\n')

                # Adding the worst fitness of each generation to the property fitnesses as this will be useful for
                # grid-search and on choosing the best method.
                self.fitnesses.append(worst_individual.fitness[0])

            if store:
                self.store(gens)
            self.gen += 1

    def store(self, num_gens):
        """Stores the fitness value of each generation for each run.

        Returns: A csv file with the info.
        """

        best_individual = max(self, key=attrgetter("fitness"))
        # Will be used to count the number of lines in the file.
        i = 0
        # Creating the file path.
        my_file = Path(fr"{self.folder}{self.filename}.csv")

        # Checking if the file exists.
        if my_file.is_file():
            # If the file exists we count the number of lines in the file.
            with open(fr"{self.folder}{self.filename}.csv") as f:
                for i, l in enumerate(f):
                    pass

        # If all the generations aren't completed, the code opens the file
        # in append mode and writes a row containing the number the generation
        # and the fitness value of that generation.
        if i < num_gens - 1:
            with open(fr"{self.folder}{self.filename}.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([self.gen, best_individual.fitness[0]])

        # If it is completed, the code opens the file in read/write mode,
        # and goes to the beginning of the file for writing.
        else:
            with open(fr"{self.folder}{self.filename}.csv", 'r+') as f:
                lines = f.readlines()
                # For each line, it checks if the first element matches
                # the generation, if it does it update that line by
                # stripping trailing whitespace and appending the fitness at the end.
                for i, line in enumerate(lines):
                    if line.split(",")[0] == f"{self.gen}":
                        lines[i] = lines[i].strip() + f",{best_individual.fitness[0]}\n"
                f.seek(0)
                # Finally, the updated lines are written back to the file by iterating
                # over them.
                for line in lines:
                    f.write(line)
                # Truncate the file to the current cursor position.
                f.truncate()

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
