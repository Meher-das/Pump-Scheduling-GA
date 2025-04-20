# constraints.py

from .evaluation import simulate_network

def check_constraints(individual, wn, time_steps):
    """
    Return True if all hydraulic constraints pass, else False.
    """
    try:
        results = simulate_network(individual, wn)
        # TODO: extract tank heads, volumes, node pressures
        # and verify they’re within limits throughout.
        return True
    except Exception:
        return False
