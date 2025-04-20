# Pump-Scheduling-GA/simulation.py

import wntr
from datetime import timedelta
import config
import numpy as np

class SimulationManager:

    # Initialize
    def __init__(self, schedule, inp_file_path=config.INP_FILE):
        self.schedule = schedule
        self.inp_file_path = inp_file_path
        self.wn = wntr.network.WaterNetworkModel(self.inp_file_path)

        self.num_pumps = self._get_num_pumps()
        self.time_steps = self._get_time_steps()
        self.results = self.run_simulation(self.schedule)

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
        results = sim.run_sim()

        self.remove_schedule()        
        self.wn.reset_initial_values()

        return results

    # Volume constraint
    def volume_constraint(self):
        pass

    # Pressure constraint
    def pressure_constraint(self):
        pass

    # Level constraint
    def level_constraint(self):
        pass

    # Objective function - 1 : Pump Energy cost 
    def objective_function_1(self, electricity_prices=[0.0244]*7+[0.1194]*15+[0.0244]*2, pump_efficiency=0.75):
        """
        Computes the total energy cost of running pumps over the simulation period.

        Parameters:
        - wn: WaterNetworkModel
        - results: Simulation results from WNTR
        - electricity_prices: List or array of electricity prices (length = time steps)
        - pump_efficiency: Efficiency of pumps (0 < η ≤ 1)

        Returns:
        - float: total cost of pump operation
        """
        gamma = 9.81  # kN/m³
        timestep = self.wn.options.time.hydraulic_timestep  # in seconds
        duration_hr = timestep / 3600

        total_cost = 0.0
        num_price_steps = len(electricity_prices)

        for pump_name in self.wn.pump_name_list:
            curve_name = self.wn.get_link(pump_name).pump_curve_name
            curve = self.wn.get_curve(curve_name)
            points = np.array(curve.points)
            flows = points[:, 0]
            heads = points[:, 1]

            pump_flows = self.results.link['flowrate'][pump_name].values

            for t, flow in enumerate(pump_flows[:num_price_steps]):
                if flow <= 0:
                    continue

                head = np.interp(flow, flows, heads)
                power_kw = (gamma * flow * head) / (pump_efficiency)  # kW

                cost = power_kw * duration_hr * electricity_prices[t]
                total_cost += cost

        return total_cost


    # Objective function - 2
    def objective_function_2(self):
        pass

    # Objective function - 3
    def objective_function_3(self):
        pass


# 🔧 Test block
if __name__ == "__main__":
    import numpy as np

    # Replace with the actual path to your .inp file
    inp_file = "Network Files/Net3.inp"  # <-- Update this path

    dummy_schedule = [
        [0, 1, 0, 1, 0, 1, 0, 1] * (24 // 8),
        [1, 0, 1, 0, 1, 0, 1, 0] * (24 // 8)
    ]

    sim_mgr = SimulationManager(dummy_schedule)

    print(f"Num pumps: {2}")
    print(f"Time steps: {24}")

    print("Running test simulation with dummy schedule...")
    print(sim_mgr.objective_function_1())
