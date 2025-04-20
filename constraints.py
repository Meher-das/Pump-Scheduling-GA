from wntr.sim import WntrSimulator
from config import TANK_HEAD_LIMITS, MIN_NODE_PRESSURE, MAX_NODE_PRESSURE, VOLUME_CHANGE_TOLERANCE

def evaluate_constraints(sim, individual_schedule):
    try:
        # Reset to initial conditions
        sim.wn.reset_initial_values()

        # Clear any existing controls
        sim.wn.control_name_list.clear()
        sim.wn._controls = []

        # Apply schedules (control) based on the individual (schedule of pump on/off states)
        for pump_name, schedule in zip(sim.pump_name_list, individual_schedule):
            pump = sim.wn.get_link(pump_name)

            for t, state in enumerate(schedule):
                status = 'OPEN' if state else 'CLOSED'
                # Add control to change the status of the pump at specific time steps
                sim.wn.add_control(
                    name=f"{pump_name}_{t}",
                    control_type='TIME',
                    control_value=t * sim.hydraulic_step,
                    element=pump_name,
                    status=status
                )

        # Run the simulation using the WntrSimulator
        simulator = WntrSimulator(sim.wn)
        results = simulator.run_sim()

        penalty = 0

        # 1. Tank head constraint
        # Iterate over all tanks and check if their heads are within specified bounds
        tank_heads = results.node['head'][sim.wn.tank_name_list]
        for tank_name, tank_head in tank_heads.items():
            # Retrieve tank specific min and max from config
            min_head = TANK_HEAD_LIMITS.get(tank_name, {}).get("min", -float("inf"))
            max_head = TANK_HEAD_LIMITS.get(tank_name, {}).get("max", float("inf"))

            if (tank_head < min_head) or (tank_head > max_head):
                penalty += 1e6  # Heavy penalty for violating tank head constraints

        # 2. Pressure head constraint for all nodes
        pressures = results.node['pressure']
        for node_name, pressure in pressures.items():
            '''
            # Retrieve node specific min and max from config
            min_pressure = NODE_PRESSURE_LIMITS.get(node_name, {}).get("min", -float("inf"))
            max_pressure = NODE_PRESSURE_LIMITS.get(node_name, {}).get("max", float("inf"))
            '''

            if (pressure < MIN_NODE_PRESSURE) or (pressure > MAX_NODE_PRESSURE):
                penalty += 1e6  # Heavy penalty for violating pressure constraints

        # 3. Tank volume change constraint
        tank_volumes = results.node['demand'][sim.wn.tank_name_list]
        start_vol = tank_volumes.iloc[0].sum()
        end_vol = tank_volumes.iloc[-1].sum()

        # Check for volume change tolerance
        if abs((end_vol - start_vol) / start_vol) > VOLUME_CHANGE_TOLERANCE:
            penalty += 1e6  # Heavy penalty for violating volume change constraint

        return penalty

    except Exception as e:
        print("[Constraint Violation] Simulation failed:", e)
        return 1e9  # Return a very high penalty if something goes wrong
