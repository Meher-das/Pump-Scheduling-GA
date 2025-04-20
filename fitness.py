# fitness.py

from .evaluation   import simulate_network
from .constraints  import check_constraints
from .utils        import count_switches_per_pump
from config        import HEAVY_PENALTY, SWITCH_PENALTY_RATE

def calculate_costs(individual, wn):
    # Run sim
    results = simulate_network(individual, wn)
    # TODO: compute electricity‐cost, demand‐charge from results
    op_cost      = 0.0
    demand_charge= 0.0
    # Switch penalty
    total_switches = sum(count_switches_per_pump(g) for g in individual)
    switch_penalty = SWITCH_PENALTY_RATE * total_switches
    return op_cost, switch_penalty, demand_charge

def evaluate(individual, wn, time_steps):
    # Check hydraulic feasibility
    if not check_constraints(individual, wn, time_steps):
        return (HEAVY_PENALTY,)
    # Compute objective parts
    op, sp, dc = calculate_costs(individual, wn)
    return (op + sp + dc,)
