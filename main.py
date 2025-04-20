# main.py

from deap         import base, tools, algorithms
import wntr, random

from config       import *
from individual   import register_types, generate_individual
from fitness      import evaluate

def main():
    # 1) Load network
    wn = wntr.network.WaterNetworkModel(INP_FILE)
    time_steps = len(wn.options.time.pattern_times)
    num_pumps   = len(wn.pump_name_list)

    # 2) GA setup
    register_types()
    toolbox = base.Toolbox()
    toolbox.register("individual",
                     generate_individual,
                     time_steps, num_pumps)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate, wn=wn, time_steps=time_steps)
    toolbox.register("mate",    tools.cxTwoPoint)
    toolbox.register("mutate",  tools.mutFlipBit, indpb=0.05)
    toolbox.register("select",  tools.selTournament, tournsize=3)

    pop = toolbox.population(n=POPULATION_SIZE)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda fits: sum(f[0] for f in fits)/len(fits))
    stats.register("min", lambda fits: min(f[0] for f in fits))
    stats.register("max", lambda fits: max(f[0] for f in fits))

    # 3) Evolve
    pop, log = algorithms.eaSimple(
        pop, toolbox,
        cxpb=0.5, mutpb=MUTATION_PROB,
        ngen=GENERATIONS,
        stats=stats, verbose=True
    )

    # 4) Output best
    best = tools.selBest(pop, 1)[0]
    print("Best fitness:", best.fitness.values[0])
    print("Best genes:", best)

if __name__ == "__main__":
    main()
