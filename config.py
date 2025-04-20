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

# Define the tank head limits (min and max for each tank) 
TANK_HEAD_LIMITS = {
    "1": {"min": 6.5, "max": 9},
    "2": {"min": 6.5, "max": 8.5},
    "3": {"min": 6.0, "max": 9.0},
    # Add more tanks as needed
}

MIN_NODE_PRESSURE = 5  # in meters
MAX_NODE_PRESSURE = 10  # in meters

# Penalty rate for each flip (if you want finer weighting)
SWITCH_PENALTY_RATE = 1.0

# Heavy penalty for infeasible solutions
HEAVY_PENALTY = 1e6

# This stays here so the rest of the code can refer to it
TIME_STEPS = 24 # None can try infering from simulation
NUM_PUMPS = 2 # None can try infering from simulation

INP_FILE = "Network Files/Net3.inp"  # <- You set this in main.py or test script
