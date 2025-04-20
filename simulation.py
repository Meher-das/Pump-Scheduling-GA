# Pump-Scheduling-GA/simulation.py

import wntr
from datetime import timedelta
from utils import add_schedule, remove_schedule

class SimulationManager:
    def __init__(self, inp_file_path):
        self.inp_file_path = inp_file_path
        self.wn = wntr.network.WaterNetworkModel(self.inp_file_path)

        self.num_pumps = self._get_num_pumps()
        self.time_steps = self._get_time_steps()

    def _get_num_pumps(self):
        return len(self.wn.pump_name_list)

    def _get_time_steps(self):
        duration_hours = self.wn.options.time.duration / 3600  # duration in hours
        hydraulic_step_hours = self.wn.options.time.hydraulic_timestep / 3600
        return int(duration_hours / hydraulic_step_hours)

    def add_schedule(self, schedule):
        for i in range(self.wn.describe(level=1)['Links']['Pumps']):
            for j in range(int(self.wn.options.time.duration / self.wn.options.time.hydraulic_timestep)):
                pump = self.wn.get_link(self.wn.pump_name_list[i])
                condition = wntr.network.controls.SimTimeCondition(self.wn, '=', str(timedelta(hours=j)))
                action = wntr.network.controls.ControlAction(pump, 'status', schedule[i][j])
                control = wntr.network.controls.Control(condition, action, name=f'Control_pump{i}_time{j}')
                self.wn.add_control(f"Control Pump ID : {i}, Hour : {j}", control)
    
    def remove_schedule(self):
        for i in range((self.wn.describe(level=1)['Links']['Pumps'])):
            for j in range(int(self.wn.options.time.duration / self.wn.options.time.hydraulic_timestep)):
                self.wn.remove_control(f"Control Pump ID : {i}, Hour : {j}")

    def run_simulation(self, schedule):
        
        self.add_schedule(schedule)

        # Run the simulation
        sim = wntr.sim.WNTRSimulator(self.wn)
        results = sim.run_sim()

        self.remove_schedule()        
        self.wn.reset_initial_values()

        return results


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