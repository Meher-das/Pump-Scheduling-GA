# evaluation.py

import wntr

def simulate_network(individual, wn):
    """
    Takes DEAP individual, decodes schedule, applies to wntr model,
    runs EPANET sim, and returns results object.
    """
    from .utils import full_binary_matrix

    schedule = full_binary_matrix(individual)
    # TODO: inject each pump’s schedule into wn.options ...
    # Example for pump i at each time t:
    # wn.get_link(pump_name).status = schedule[i][t]
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    return results
