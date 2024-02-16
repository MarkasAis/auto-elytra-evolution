import math
import threading
from random import random

import numpy as np
from geneticalgorithm import geneticalgorithm as ga

from controller import evaluate
from visualizer import visualize

MAX_NUM_ITERATIONS = 3000
POPULATION_SIZE = 100
MUTATION_PROBABILITY = 0.05
ELIT_RATIO = 0.05
CROSSOVER_PROBABILITY = 0.5
PARENTS_PORTION = 0.3
CROSSOVER_TYPE = 'uniform'

best_fitness = -math.inf
total_genome_count = 0


def error(solution):
    global best_fitness
    global total_genome_count

    total_genome_count += 1

    # print(solution)

    if random() < 0.05:
        visualize(solution)
        # print(solution)
        pass

    fitness, _ = evaluate(solution)

    if fitness > best_fitness:
        print(f"\nHighest fitness: {fitness}\nSolution: {solution}\n")
        best_fitness = fitness

        visualize(solution)

    return -fitness


def get_generation_count():
    return total_genome_count // POPULATION_SIZE + 1


varbound = np.array([[0, 90], [0, 10], [0, 10], [-90, 0], [1, 10], [1, 10]])

algorithm_param = {'max_num_iteration': MAX_NUM_ITERATIONS,
                   'population_size': POPULATION_SIZE,
                   'mutation_probability': MUTATION_PROBABILITY,
                   'elit_ratio': ELIT_RATIO,
                   'crossover_probability': CROSSOVER_PROBABILITY,
                   'parents_portion': PARENTS_PORTION,
                   'crossover_type': CROSSOVER_TYPE,
                   'max_iteration_without_improv': None}

model = ga(function=error,
           dimension=6,
           variable_type='real',
           variable_boundaries=varbound,
           algorithm_parameters=algorithm_param)


class GAThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        model.run()


def run():
    ga_thread = GAThread()
    ga_thread.start()
