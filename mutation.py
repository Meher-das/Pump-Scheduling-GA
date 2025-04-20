import random
from config import SWITCH_LIMITS
from config import TIME_STEPS
from copy import deepcopy


def mutate_individual(individual, time_steps = TIME_STEPS, max_switches=SWITCH_LIMITS["max"], mutpb=0.2):
    from copy import deepcopy
    mutant = deepcopy(individual)

    for i in range(len(mutant)):  # for each pump
        # Flip initial state
        if random.random() < mutpb:
            mutant[i][0] ^= 1  # flip 0 <-> 1

        # Mutate switch positions
        switches = mutant[i][1]
        real_switches = [s for s in switches if s != 0]

        for j in range(len(real_switches)):
            if random.random() < mutpb:
                # Randomly perturb by ±1 step (within bounds)
                delta = random.choice([-1, 1])
                new_pos = real_switches[j] + delta
                real_switches[j] = max(1, min(time_steps - 1, new_pos))

            if random.random() < 0.1:
                # Occasionally replace with a completely random new switch
                real_switches[j] = random.randint(1, time_steps - 1)

        # Optional: randomly add or remove a switch
        if len(real_switches) < max_switches and random.random() < 0.2:
            new_switch = random.randint(1, time_steps - 1)
            if new_switch not in real_switches:
                real_switches.append(new_switch)

        if len(real_switches) > 1 and random.random() < 0.2:
            real_switches.pop(random.randrange(len(real_switches)))

        # Clean up and pad
        real_switches = sorted(set(real_switches))[:max_switches]
        padded = real_switches + [0] * (max_switches - len(real_switches))
        mutant[i][1] = padded

    return mutant,

'''
ind1 = [
    [1, [2, 5, 8, 0, 0]],
    [0, [3, 7, 9, 0, 0]]
]

mutant = mutate_individual(ind1)
print("Original:", ind1)
print("Mutant:", mutant)
'''