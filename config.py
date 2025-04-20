# config.py

POPULATION_SIZE = 100
GENERATIONS = 100
MUTATION_PROB = 0.167
SWITCH_LIMITS = {
    "min": 0,  # Set later
    "max": 5   # Set later
}

# This stays here so the rest of the code can refer to it
TIME_STEPS = None
NUM_PUMPS = None


INP_FILE = ""  # <- You set this in main.py or test script

# Define the tank head limits (min and max for each tank) 
TANK_HEAD_LIMITS = {
    "1": {"min": 6.5, "max": 9},
    "2": {"min": 6.5, "max": 8.5},
    "3": {"min": 6.0, "max": 9.0},
    # Add more tanks as needed
}

MIN_NODE_PRESSURE = 5  # in meters
MAX_NODE_PRESSURE = 10  # in meters

# Define the volume change tolerance
VOLUME_CHANGE_TOLERANCE = 0.1  # 5% change in volume
