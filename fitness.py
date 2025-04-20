import random 
from constraints import evaluate_constraints

def dummy_fitness(individual):
    return (random.uniform(0, 100),)