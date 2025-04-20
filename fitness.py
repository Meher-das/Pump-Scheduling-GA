import random 
from simulation import SimulationManager
import utils
import config

def fitness(individual):
    
    schedule = utils.full_binary_matrix(individual, config.TIME_STEPS)
    sim = SimulationManager(schedule)    

    return sim.objective_function_1(),