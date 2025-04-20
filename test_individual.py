# test_individual.py

from simulation import SimulationManager
import config

def test_individual():
    sim = SimulationManager(config.INP_FILE)

    # Inject dynamically loaded config values
    config.TIME_STEPS = sim.time_steps
    config.NUM_PUMPS = sim.num_pumps

    from individual import generate_individual
    from utils import decode_schedule, count_switches_per_pump

    print("🔧 Testing individual generation and decoding...")
    individual = generate_individual(config.TIME_STEPS, config.NUM_PUMPS)

    for i, pump_gene in enumerate(individual):
        print(f"\n🚰 Pump {i+1} Gene:")
        print(f"Initial State: {pump_gene[0]}")
        print(f"Switch Positions (padded): {pump_gene[1]}")
        print(f"Actual Switch Count: {count_switches_per_pump(pump_gene)}")

        schedule = decode_schedule(pump_gene, config.TIME_STEPS)
        print(f"Decoded Schedule (length: {len(schedule)}):")
        print(schedule)

        assert len(schedule) == config.TIME_STEPS

if __name__ == "__main__":
    test_individual()
