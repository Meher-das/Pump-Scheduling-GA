# utils.py
import wntr

def decode_schedule(pump_gene, time_steps):
    initial_state, padded_flips = pump_gene
    flip_positions = sorted([p for p in padded_flips if p > 0])  # ignore 0s

    schedule = []
    current_state = initial_state
    flip_positions.append(time_steps)

    prev = 0
    for flip in flip_positions:
        section_length = flip - prev
        schedule.extend([current_state] * section_length)
        current_state ^= 1
        prev = flip

    return schedule

def full_binary_matrix(individual, time_steps):
    return [decode_schedule(g, time_steps) for g in individual]

def count_switches_per_pump(pump_gene):
    _, padded_flips = pump_gene
    return sum(1 for p in padded_flips if p > 0)

def add_schedule(wntk, schedule):
    for i in range(wntk.describe(level=1)['Links']['Pumps']):
        for j in range(int(wntk.options.time.duration / wntk.options.time.hydraulic_timestep) + 1):
            pump = wntk.get_link(wntk.pump_name_list[i])
            condition = wntr.network.controls.SimTimeCondition(wntk, '=', str(timedelta(hours=j)))
            action = wntr.network.controls.ControlAction(pump, 'status', schedule[i][j])
            control = wntr.network.controls.Control(condition, action, name=f'Control_pump{i}_time{j}')
            wntk.add_control(f"Control Pump ID : {i}, Hour : {j}", control)

def remove_schedule(wntk):
    for i in range(wntk.describe(level=1)['Links']['Pumps']):
        for j in range(int(wntk.options.time.duration / wntk.options.time.hydraulic_timestep) + 1):
            wntk.remove_control(f"Control Pump ID : {i}, Hour : {j}")