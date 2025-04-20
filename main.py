# main.py

from deap import base, tools, algorithms
import wntr
import random

from config import *
from individual import register_types, generate_individual
from fitness import evaluate

def main():
    wn = wntr.network.WaterNetworkModel(INP_FILE)
    time_steps = len(wn.options.time.pattern_times)
    num_pumps = len(wn.pump_name_list)

    register_types()
    toolbox = base.Toolbox()

    toolbox.register("individual", generate_individual, time_steps, num_pumps, SWITCH_LIMITS)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate, wn=wn, time_steps=time_steps)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=POPULATION_SIZE)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda x: sum(x)/len(x))
    stats.register("min", min)
    stats.register("max", max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=MUTATION_PROB,
                                   ngen=GENERATIONS, stats=stats, verbose=True)

    best = tools.selBest(pop, k=1)[0]
    print("Best solution:", best)
    print("Fitness:", best.fitness.values)

if __name__ == "__main__":
    main()
