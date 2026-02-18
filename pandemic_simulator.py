import random

if __name__ == "__main__":
    # Age groups (scaled down for speed)
    # Example: children, adults, elderly
    population_groups = {
        "children": 2000000,
        "adults": 5000000,
        "elderly": 1275200
    }

    # Initial infected per group
    infected_groups = {
        "children": 1,
        "adults": 1,
        "elderly": 0
    }

    deaths_groups = {
        "children": 0,
        "adults": 0,
        "elderly": 0
    }

    # Base parameters per group
    infection_rate_groups = {
        "children": 0.10,   # children less likely to spread
        "adults": 0.15,
        "elderly": 0.12
    }

    mortality_rate_groups = {
        "children": 0.001,  # very low mortality
        "adults": 0.01,
        "elderly": 0.05     # higher mortality
    }

    # Virus and simulation parameters
    mutation_probability = 0.002
    progress_toward_cure = 0.2
    chance_of_progress_setback = 0.001
    chance_of_breakthrough = 0.0001
    birth_rate = 0.0161

    number_of_universes = 100
    simulation_per_universe = 1000

    hospital_capacity = 0.01 * sum(population_groups.values())
    vaccination_rollout_rate = 0.01
    max_mortality_increase = 0.05

    # Track stats
    peak_infected_per_universe = []
    yearly_infected_history = []
