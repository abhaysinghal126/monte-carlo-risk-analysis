import random

def mutation(mutation_probability:float, progress_toward_cure:float, infection_rate_groups: dict, mortality_rate_groups:dict ) -> tuple:

    if(random.uniform(0,1) < mutation_probability):

        setback = random.uniform(0.001, progress_toward_cure)
        progress_toward_cure = max(0, progress_toward_cure-setback)

        for group in infection_rate_groups:
            change_in_infection_rate = random.uniform(random.uniform(-0.05, -0.01), random.uniform(0.01, 0.05))
            infection_rate_groups[group] += min(max(infection_rate_groups[group] + change_in_infection_rate, 0), 1)

        for group in mortality_rate_groups:
            change_in_mortality_rate = random.uniform(random.uniform(-0.05, -0.01), random.uniform(0.01, 0.05))
            mortality_rate_groups[group] += min(max(mortality_rate_groups[group] + change_in_mortality_rate, 0), 1)

    return progress_toward_cure, infection_rate_groups, mortality_rate_groups

def simulate_year(population_groups: list,
                  infected_groups: list,
                  death_groups: list,
                  infection_rate_groups: list,
                  mortality_rate_group: list,
                  mutation_probability: float,
                  progress_toward_cure: float,
                  chance_of_progress_setback: float,
                  chance_of_breakthrough: float,
                  birth_rate: float,
                  hospital_capacity: float,
                  vaccination_rollout_rate: float,
                  max_mortality_increase: float,
                  ):
    pass

def run_universe(population_groups: list,
                  infected_groups: list,
                  death_groups: list,
                  infection_rate_groups: list,
                  mortality_rate_group: list,
                  mutation_probability: float,
                  progress_toward_cure: float,
                  chance_of_progress_setback: float,
                  chance_of_breakthrough: float,
                  birth_rate: float,
                  hospital_capacity: float,
                  vaccination_rollout_rate: float,
                  max_mortality_increase: float,
                  simulation_per_universe: float
                  ):
    pass

def analysis(population_groups: list,
                  infected_groups: list,
                  death_groups: list,
                  infection_rate_groups: list,
                  mortality_rate_group: list,
                  mutation_probability: float,
                  progress_toward_cure: float,
                  chance_of_progress_setback: float,
                  chance_of_breakthrough: float,
                  birth_rate: float,
                  hospital_capacity: float,
                  vaccination_rollout_rate: float,
                  max_mortality_increase: float,
                  simulation_per_universe: float,
                  number_of_universes: float
                  ):
    pass


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
