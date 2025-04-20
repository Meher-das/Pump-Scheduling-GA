import wntr
import pandas as pd
from utils import add_schedule, remove_schedule
from config import TANK_HEAD_LIMITS, MIN_NODE_PRESSURE, MAX_NODE_PRESSURE

def evaluate_constraints(sim, individual_schedule):
    
    add_schedule(sim, individual_schedule)









    '''
    from wntr.sim import WNTRSimulator
    simulator = WNTRSimulator(sim.wn)
    results = simulator.run_sim()

    penalty = 0

    # ✅ Tank head constraint
    tank_heads = results.node['head']
    for tank_id, limits in TANK_HEAD_LIMITS.items():
        if tank_id in tank_heads.columns:
            series = tank_heads[tank_id]
            if ((series < limits["min"]) | (series > limits["max"])).any():
                penalty += 1e6

    # ✅ Pressure constraints (common to all nodes)
    pressures = results.node['pressure']
    if ((pressures < MIN_NODE_PRESSURE) | (pressures > MAX_NODE_PRESSURE)).any().any():
        penalty += 1e6

    # ✅ Volume change constraint
    volumes = results.node['demand'][sim.wn.tank_name_list]
    start_vol = volumes.iloc[0].sum()
    end_vol = volumes.iloc[-1].sum()
    if abs((end_vol - start_vol) / start_vol) > sim.volume_change_tol:
        penalty += 1e6

    return penalty
    '''