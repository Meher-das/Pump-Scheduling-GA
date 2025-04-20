# config.py

POPULATION_SIZE = 100
GENERATIONS     = 100
MUTATION_PROB   = 0.167

# Switch‐count constraints (min/max flips per pump)
# Set these before running
SWITCH_LIMITS = {
    "min": 0,
    "max": 5
}

# Penalty rate for each flip (if you want finer weighting)
SWITCH_PENALTY_RATE = 1.0

# Heavy penalty for infeasible solutions
HEAVY_PENALTY = 1e6

# This stays here so the rest of the code can refer to it
TIME_STEPS = None
NUM_PUMPS = None

INP_FILE = ""  # <- You set this in main.py or test script
