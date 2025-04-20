import wntr
import pandas as pd
from evaluation import simulate_network
from utils import add_schedule, remove_schedule
from config import TANK_HEAD_LIMITS, MIN_NODE_PRESSURE, MAX_NODE_PRESSURE

def evaluate_constraints(sim, individual_schedule):
    pass