from deap import algorithms, base, creator, tools
import random
import config
from individual import generate_individual
from fitness import fitness
from mutation import mutate_individual
from crossover import uniform_crossover
from utils import full_binary_matrix

try:
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
except:
    pass

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, lambda: generate_individual(config.TIME_STEPS, config.NUM_PUMPS))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", fitness)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", uniform_crossover)
toolbox.register("mutate", mutate_individual)

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

if __name__ == "__main__":
    run_evolution()