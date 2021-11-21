import pygad
import matplotlib.pyplot as plt

from src.controller import evaluate, denormalize

plt.ion()

num_generations = 20
num_parents_mating = 7

sol_per_pop = 30
num_genes = 6


def fitness_function(solution, solution_idx):
    fitness, x, y = evaluate(solution)
    return fitness


last_fitness = 0
def callback_generation(ga_instance):
    global last_fitness
    print("Generation   : {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness      : {fitness}".format(fitness=ga_instance.best_solution()[1]))
    print("Change       : {change}".format(change=ga_instance.best_solution()[1] - last_fitness))
    last_fitness = ga_instance.best_solution()[1]

    best_coefficients = ga_instance.best_solution()[0]
    print("Coefficients : {coefficients}".format(coefficients=best_coefficients))
    print("Denormalized : {coefficients}".format(coefficients=denormalize(best_coefficients)))
    print("")

    _, x, y = evaluate(best_coefficients)
    plt.plot(x, y)
    plt.draw()
    plt.pause(0.0001)


ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       on_generation=callback_generation,
                       init_range_low=-0.5,
                       init_range_high=0.5,
                       random_mutation_min_val=-0.15,
                       random_mutation_max_val=0.15)


ga_instance.run()


# ga_instance.plot_fitness()
#
# # Returning the details of the best solution.
# solution, solution_fitness, solution_idx = ga_instance.best_solution()
# print("Parameters of the best solution : {solution}".format(solution=solution))
# print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
# print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))
#
# if ga_instance.best_solution_generation != -1:
#     print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))
#
# # Saving the GA instance.
# filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
# ga_instance.save(filename=filename)
#
# # Loading the saved GA instance.
# loaded_ga_instance = pygad.load(filename=filename)
# loaded_ga_instance.plot_fitness()