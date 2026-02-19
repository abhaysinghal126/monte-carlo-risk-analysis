import random

def mutation(
    mutation_probability: float,
    progress_toward_cure: float,
    infection_rate_groups: dict,
    mortality_rate_groups: dict
) -> tuple:
    """Apply mutation effects on infection and mortality rates, and progress toward cure."""
    if random.random() < mutation_probability:
        # Progress setback
        setback = random.uniform(0.001, progress_toward_cure)
        progress_toward_cure = max(0.0, progress_toward_cure - setback)

        # Infection rate changes
        for group in infection_rate_groups:
            delta = random.uniform(-0.08, 0.8)
            infection_rate_groups[group] = min(max(infection_rate_groups[group] + delta, 0.0), 1.0)

        # Mortality rate changes
        for group in mortality_rate_groups:
            delta = random.uniform(-0.5, 0.5)
            mortality_rate_groups[group] = min(max(mortality_rate_groups[group] + delta, 0.0), 1.0)

    return progress_toward_cure, infection_rate_groups, mortality_rate_groups


def simulate_year(
    population_groups: dict,
    infected_groups: dict,
    death_groups: dict,
    infection_rate_groups: dict,
    mortality_rate_groups: dict,
    mutation_probability: float,
    progress_toward_cure: float,
    chance_of_progress_setback: float,
    chance_of_breakthrough: float,
    birth_rate: float,
    hospital_capacity: float,
    vaccination_rollout_rate: float,
    max_mortality_increase: float
) -> tuple:

    total_population = sum(population_groups.values())
    total_infected = sum(infected_groups.values())

    # Hospital overload effect
    mortality_multiplier = 1.0
    if total_infected > hospital_capacity:
        overload_ratio = (total_infected - hospital_capacity) / hospital_capacity
        mortality_multiplier += min(overload_ratio, max_mortality_increase)

    for group in population_groups:
        susceptible = population_groups[group] - infected_groups[group]
        infection_pressure = random.uniform(0.7,1)

        # New infections
        new_infection = sum(
            1 for _ in range(susceptible)
            if random.random() < infection_rate_groups[group] * infection_pressure * (1.0 - progress_toward_cure)
        )

        # Breakthrough infections
        if random.random() < chance_of_breakthrough:
            new_infection = int(0.001 * susceptible)

        # Deaths and recoveries
        effective_mortality = mortality_rate_groups[group] * mortality_multiplier
        deaths = int(effective_mortality * infected_groups[group])
        recoveries = int(progress_toward_cure * infected_groups[group])

        # Update counts
        infected_groups[group] += new_infection - deaths - recoveries
        infected_groups[group] = max(infected_groups[group], 0)
        death_groups[group] += deaths
        population_groups[group] -= deaths

        # Births
        if group == "adults":
            births = int(population_groups[group] * birth_rate)
            population_groups["children"] += births

        # Mutations
        progress_toward_cure, infection_rate_groups, mortality_rate_groups = mutation(
            mutation_probability,
            progress_toward_cure,
            infection_rate_groups,
            mortality_rate_groups
        )

        # Vaccination and setbacks
        progress_toward_cure = min(progress_toward_cure + vaccination_rollout_rate, 1.0)
        if random.random() < chance_of_progress_setback:
            progress_toward_cure *= 0.9

    return population_groups, infected_groups, death_groups, infection_rate_groups, progress_toward_cure, mortality_rate_groups


def run_universe(
    population_groups: dict,
    infected_groups: dict,
    death_groups: dict,
    infection_rate_groups: dict,
    mortality_rate_groups: dict,
    mutation_probability: float,
    progress_toward_cure: float,
    chance_of_progress_setback: float,
    chance_of_breakthrough: float,
    birth_rate: float,
    hospital_capacity: float,
    vaccination_rollout_rate: float,
    max_mortality_increase: float,
    simulation_per_universe: int
) -> dict:

    # Make copies to avoid modifying originals
    population = population_groups.copy()
    infected = infected_groups.copy()
    deaths = death_groups.copy()
    infection_rate = infection_rate_groups.copy()
    mortality_rate = mortality_rate_groups.copy()
    progress = progress_toward_cure

    peak_infected = sum(infected.values())
    yearly_history = []

    for year in range(simulation_per_universe):
        population, infected, deaths, infection_rate, progress, mortality_rate = simulate_year(
            population,
            infected,
            deaths,
            infection_rate,
            mortality_rate,
            mutation_probability,
            progress,
            chance_of_progress_setback,
            chance_of_breakthrough,
            birth_rate,
            hospital_capacity,
            vaccination_rollout_rate,
            max_mortality_increase
        )

        total_infected = sum(infected.values())
        peak_infected = max(peak_infected, total_infected)

        yearly_history.append({
            "year": year,
            "total_population": sum(population.values()),
            "total_infected": total_infected,
            "total_deaths": sum(deaths.values())
        })

        if total_infected == 0:
            break

    return {
        "final_population": sum(population.values()),
        "final_infected": sum(infected.values()),
        "total_deaths": sum(deaths.values()),
        "peak_infected": peak_infected,
        "years_simulated": len(yearly_history),
        "history": yearly_history
    }


def analysis(
    population_groups: dict,
    infected_groups: dict,
    death_groups: dict,
    infection_rate_groups: dict,
    mortality_rate_groups: dict,
    mutation_probability: float,
    progress_toward_cure: float,
    chance_of_progress_setback: float,
    chance_of_breakthrough: float,
    birth_rate: float,
    hospital_capacity: float,
    vaccination_rollout_rate: float,
    max_mortality_increase: float,
    simulation_per_universe: int,
    number_of_universes: int
) -> dict:

    final_infected_list = []
    total_deaths_list = []
    peak_infected_list = []
    years_simulated_list = []

    for _ in range(number_of_universes):
        universe_result = run_universe(
            population_groups,
            infected_groups,
            death_groups,
            infection_rate_groups,
            mortality_rate_groups,
            mutation_probability,
            progress_toward_cure,
            chance_of_progress_setback,
            chance_of_breakthrough,
            birth_rate,
            hospital_capacity,
            vaccination_rollout_rate,
            max_mortality_increase,
            simulation_per_universe
        )

        final_infected_list.append(universe_result["final_infected"])
        total_deaths_list.append(universe_result["total_deaths"])
        peak_infected_list.append(universe_result["peak_infected"])
        years_simulated_list.append(universe_result["years_simulated"])

    return {
        "average_final_infected": sum(final_infected_list) / number_of_universes,
        "average_total_deaths": sum(total_deaths_list) / number_of_universes,
        "average_peak_infected": sum(peak_infected_list) / number_of_universes,
        "average_years_simulated": sum(years_simulated_list) / number_of_universes,
        "probability_extinction": sum(1 for x in final_infected_list if x == 0) / number_of_universes,
        "probability_hospital_overload": sum(1 for x in peak_infected_list if x > hospital_capacity) / number_of_universes
    }

if __name__ == "__main__":
    # Age groups (scaled down for speed)
    # Example: children, adults, elderly
    population_groups = {
        "children": 200000,
        "adults": 500000,
        "elderly": 127520
    }

    # Initial infected per group
    infected_groups = {
        "children": 1,
        "adults": 1,
        "elderly": 1
    }

    deaths_groups = {
        "children": 0,
        "adults": 0,
        "elderly": 0
    }

    # Base parameters per group
    infection_rate_groups = {
        "children": 0.20,   # children less likely to spread
        "adults": 0.15,
        "elderly": 0.52
    }

    mortality_rate_groups = {
        "children": 0.01,  # very low mortality
        "adults": 0.01,
        "elderly": 0.05     # higher mortality
    }

    # Virus and simulation parameters
    mutation_probability = 0.002
    progress_toward_cure = 0.2
    chance_of_progress_setback = 0.001
    chance_of_breakthrough = 0.0001
    birth_rate = 0.0161

    number_of_universes = 10
    simulation_per_universe = 40

    hospital_capacity = 0.01 * sum(population_groups.values())
    vaccination_rollout_rate = 0.01
    max_mortality_increase = 0.5

    # Track stats
    peak_infected_per_universe = []
    yearly_infected_history = []

    result = analysis(
        population_groups,
        infected_groups,
        deaths_groups,
        infection_rate_groups,
        mortality_rate_groups,
        mutation_probability,
        progress_toward_cure,
        chance_of_progress_setback,
        chance_of_breakthrough,
        birth_rate,
        hospital_capacity,
        vaccination_rollout_rate,
        max_mortality_increase,
        simulation_per_universe,
        number_of_universes
    )
    print(result)

