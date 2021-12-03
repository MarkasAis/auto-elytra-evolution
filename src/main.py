import threading
import time

import numpy as np
from geneticalgorithm import geneticalgorithm as ga

from src.controller import evaluate
import src.visualizer as vis


def f(solution):
    # return np.sum(X)
    vis.visualize(solution)
    fitness, _ = evaluate(solution)
    time.sleep(0.01)
    return fitness


varbound = np.array([[0, 90], [0, 10], [0, 10], [-90, 0], [1, 10], [1, 10]])

algorithm_param = {'max_num_iteration': 3000,
                   'population_size': 100,
                   'mutation_probability': 0.1,
                   'elit_ratio': 0.05,
                   'crossover_probability': 0.5,
                   'parents_portion': 0.3,
                   'crossover_type': 'uniform',
                   'max_iteration_without_improv': None}

model = ga(function=f,
           dimension=6,
           variable_type='real',
           variable_boundaries=varbound,
           algorithm_parameters=algorithm_param)

# model.run()


class GAThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        model.run()


ga_thread = GAThread()
ga_thread.start()

vis.run()
