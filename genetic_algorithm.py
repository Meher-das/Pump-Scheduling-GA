from deap import algorithms, base, creator, tools
import random
from individual import generate_individual, register_types
from fitness import dummy_fitness
from mutation import dummy_mutation
from crossover import uniform_crossover

register_types()

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, generate_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", dummy_fitness)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", uniform_crossover)
toolbox.register("mutate", dummy_mutation, indpb=0.1)

# GA runner using eaSimple
def run_evolution(pop_size=10, generations=5, cxpb=0.7, mutpb=0.2):
    pop = toolbox.population(n=pop_size)

    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", lambda x: sum(x)/len(x))
    stats.register("min", min)
    stats.register("max", max)

    pop, log = algorithms.eaSimple(
        population=pop,
        toolbox=toolbox,
        cxpb=cxpb,
        mutpb=mutpb,
        ngen=generations,
        stats=stats,
        verbose=True
    )

    return pop, log
