# fitness.py

from .evaluation import simulate_network
from .constraints import check_constraints
from .utils import calculate_costs

HEAVY_PENALTY = 1e6

def evaluate(individual, wn, time_steps):
    feasible = check_constraints(individual, wn, time_steps)
    if not feasible:
        return (HEAVY_PENALTY,)

    op_cost, switch_penalty, demand_charge = calculate_costs(individual, wn)
    total_cost = op_cost + switch_penalty + demand_charge
    return (total_cost,)
