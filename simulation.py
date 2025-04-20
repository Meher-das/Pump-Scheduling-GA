# Pump-Scheduling-GA/simulation.py

import wntr

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
