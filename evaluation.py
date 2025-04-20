# evaluation.py

import wntr
import numpy as np

def simulate_network(individual, wn):
    # Apply the pump schedule to the wntr model
    # Run simulation and return the simulation results
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    return results
