import random

def dummy_mutation(individual, indpb):
    for i in range(len(individual[2])):
        if random.random() < indpb:
            individual[2][i] = random.randint(1, 48)
    return (individual,)