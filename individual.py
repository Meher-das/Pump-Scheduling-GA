import random
from deap import base, creator
from config import SWITCH_LIMITS

def generate_pump_gene(time_steps):
    min_sw = SWITCH_LIMITS["min"]
    max_sw = SWITCH_LIMITS["max"]

    initial_state = random.randint(0, 1)
    switch_count = random.randint(min_sw, max_sw)

    if switch_count > 0:
        positions = sorted(random.sample(range(1, time_steps), switch_count))
        padded_positions = positions + [0] * (max_sw - switch_count)
    else:
        padded_positions = [0] * max_sw

    return (initial_state, padded_positions)

def generate_individual(time_steps, num_pumps):
    return [generate_pump_gene(time_steps) for _ in range(num_pumps)]
