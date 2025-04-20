import wntr
from config import TANK_HEAD_LIMITS, MIN_NODE_PRESSURE, MAX_NODE_PRESSURE 

class SimulationManager:
    def __init__(self, inp_file):
        self.wn = wntr.network.WaterNetworkModel(inp_file)

        # Load the tank and node limits from the config
        self.tank_head_min = TANK_HEAD_LIMITS
        self.pressure_min = MIN_NODE_PRESSURE
        self.pressure_max = MAX_NODE_PRESSURE

        # Extract time parameters from the network file
        self.sim_duration = self.wn.options.time.duration  # in seconds
        self.hydraulic_step = self.wn.options.time.hydraulic_timestep  # in seconds

        # Other necessary attributes like pumps, etc.
        self.pump_name_list = [link for link in self.wn.links if isinstance(self.wn.get_link(link), wntr.network.elements.Pump)]
        self.TIME_STEPS = self.sim_duration // self.hydraulic_step
        self.NUM_PUMPS = len(self.pump_name_list)

    def add_control(self, name, control_type, control_value, element, status):
        # Add controls to the water network model here (this is just an example)
        pass
