# Pump-Scheduling-GA/simulation.py

import wntr
from datetime import timedelta
from utils import add_schedule, remove_schedule

class SimulationManager:

    # Initialize
    def __init__(self, inp_file_path):
        self.inp_file_path = inp_file_path
        self.wn = wntr.network.WaterNetworkModel(self.inp_file_path)

        self.num_pumps = self._get_num_pumps()
        self.time_steps = self._get_time_steps()

    # Number of pumps 
    def _get_num_pumps(self):
        return len(self.wn.pump_name_list)

    # Number of time steps
    def _get_time_steps(self):
        duration_hours = self.wn.options.time.duration / 3600  # duration in hours
        hydraulic_step_hours = self.wn.options.time.hydraulic_timestep / 3600
        return int(duration_hours / hydraulic_step_hours)

    # Adding given schedule to the simulation
    def add_schedule(self, schedule):
        for i in range(self.wn.describe(level=1)['Links']['Pumps']):
            for j in range(int(self.wn.options.time.duration / self.wn.options.time.hydraulic_timestep)):
                pump = self.wn.get_link(self.wn.pump_name_list[i])
                condition = wntr.network.controls.SimTimeCondition(self.wn, '=', str(timedelta(hours=j)))
                action = wntr.network.controls.ControlAction(pump, 'status', schedule[i][j])
                control = wntr.network.controls.Control(condition, action, name=f'Control_pump{i}_time{j}')
                self.wn.add_control(f"Control Pump ID : {i}, Hour : {j}", control)
    
    # Removing Previously added schedule from simulation
    def remove_schedule(self):
        for i in range((self.wn.describe(level=1)['Links']['Pumps'])):
            for j in range(int(self.wn.options.time.duration / self.wn.options.time.hydraulic_timestep)):
                self.wn.remove_control(f"Control Pump ID : {i}, Hour : {j}")

    # Running the simulation with the given schedule
    def run_simulation(self, schedule):
        
        self.add_schedule(schedule)

        # Run the simulation
        sim = wntr.sim.WNTRSimulator(self.wn)
        self.results = sim.run_sim()

        self.remove_schedule()        
        self.wn.reset_initial_values()

        return self.results

    # Volume constraint
    def volume_constraint(self):
        pass

    # Pressure constraint
    def pressure_constraint(self):
        pass

    # Level constraint
    def level_constraint(self):
        pass

    # Objective function - 1
    def objective_function_1(self):
        pass

    # Objective function - 2
    def objective_function_2(self):
        pass

    # Objective function - 3
    def objective_function_3(self):
        pass

'''
# 🔧 Test block
if __name__ == "__main__":
    import numpy as np

    # Replace with the actual path to your .inp file
    inp_file = "Network Files/Net3.inp"  # <-- Update this path

    sim_mgr = SimulationManager(inp_file)

    print(f"Num pumps: {sim_mgr.num_pumps}")
    print(f"Time steps: {sim_mgr.time_steps}")

    dummy_schedule = [
        [0, 1, 0, 1, 0, 1, 0, 1] * (sim_mgr.time_steps // 8),
        [1, 0, 1, 0, 1, 0, 1, 0] * (sim_mgr.time_steps // 8)
    ]

    print("Running test simulation with dummy schedule...")
    results = sim_mgr.run_simulation(dummy_schedule)
    print("Done")

    print("Results head (pressure):")
    print(results.node['pressure'].head())
'''