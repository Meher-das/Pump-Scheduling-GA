import random
from copy import deepcopy
import config

MAX_SWITCHES = config.SWITCH_LIMITS["max"]   # You can import this from config

def two_point_crossover(ind1, ind2, indcxpb=0.5):
    child1, child2 = deepcopy(ind1), deepcopy(ind2)

    for i in range(len(ind1)):  # Each pump
        init1, sw1 = child1[i]
        init2, sw2 = child2[i]

        # 50% chance to swap initial state
        if random.random() < indcxpb:
            child1[i][0], child2[i][0] = init2, init1

        # Extract effective switch positions (non-zero)
        eff1 = [x for x in sw1 if x > 0]
        eff2 = [x for x in sw2 if x > 0]

        # Two-point crossover on the effective parts
        if len(eff1) > 1 and len(eff2) > 1:
            cxpoint1 = random.randint(0, min(len(eff1), len(eff2)) - 1)
            cxpoint2 = random.randint(cxpoint1, min(len(eff1), len(eff2)) - 1)

            new_eff1 = eff1[:cxpoint1] + eff2[cxpoint1:cxpoint2] + eff1[cxpoint2:]
            new_eff2 = eff2[:cxpoint1] + eff1[cxpoint1:cxpoint2] + eff2[cxpoint2:]

            # Truncate/pad to MAX_SWITCHES
            new_eff1 = sorted(list(set(new_eff1)))[:MAX_SWITCHES]
            new_eff2 = sorted(list(set(new_eff2)))[:MAX_SWITCHES]

        else:
            new_eff1, new_eff2 = eff1, eff2

        # Pad with zeros
        child1[i][1] = new_eff1 + [0] * (MAX_SWITCHES - len(new_eff1))
        child2[i][1] = new_eff2 + [0] * (MAX_SWITCHES - len(new_eff2))

    return child1, child2

def uniform_crossover(ind1, ind2, indpb=0.5):
    from copy import deepcopy
    child1, child2 = deepcopy(ind1), deepcopy(ind2)

    for i in range(len(ind1)):  # for each pump
        # Initial state swap
        if random.random() < indpb:
            child1[i][0], child2[i][0] = child2[i][0], child1[i][0]

        # Uniform crossover on padded switch positions
        sw1 = child1[i][1]
        sw2 = child2[i][1]

        new_sw1, new_sw2 = [], []

        for p1, p2 in zip(sw1, sw2):
            if random.random() < indpb:
                new_sw1.append(p2)
                new_sw2.append(p1)
            else:
                new_sw1.append(p1)
                new_sw2.append(p2)

        # Clean up and pad
        def clean_switches(switches):
            cleaned = sorted(set(filter(lambda x: x != 0, switches)))
            return cleaned[:MAX_SWITCHES] + [0] * (MAX_SWITCHES - len(cleaned))

        child1[i][1] = clean_switches(new_sw1)
        child2[i][1] = clean_switches(new_sw2)

    return child1, child2

'''
# Example individuals with 2 pumps each
ind1 = [
    [1, [2, 5, 8, 0, 0]],
    [0, [3, 7, 9, 0, 0]]
]

ind2 = [
    [0, [1, 4, 6,  0, 0]],
    [1, [2, 6, 10, 0, 0]]
]

if __name__ == "__main__":
    print("Parent 1:", ind1)
    print("Parent 2:", ind2)

    offspring1, offspring2 = uniform_crossover(ind1, ind2)

    print("Offspring 1:", offspring1)
    print("Offspring 2:", offspring2)
'''