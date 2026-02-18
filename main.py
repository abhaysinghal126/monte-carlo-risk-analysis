import random

def is_success(probability: float) -> bool:
    if not 0 <= probability <= 1:
        raise ValueError("Probablity must be between 0 and 1.")
    return random.random() < probability

def simulator(probability: float, reward: float, penalty: float, number_of_simulations: int) -> dict:

    if not isinstance(number_of_simulations, int):
        raise ValueError("The type of the number of simulations must be an integer")
    if not 0 < number_of_simulations:
        raise ValueError("The number of simulations must be greater than 0.")

    success = 0
    failure = 0
    result = []

    for _ in range (number_of_simulations):
        if(is_success(probability)):
            success += 1
            result.append(reward)
        else:
            failure += 1
            result.append(penalty)

    total = sum(result)
    average = total/number_of_simulations
    profitable = sum(1 for r in result if r > 0)
    rate_of_profitability = profitable/number_of_simulations
    success_rate = success/number_of_simulations

    return {
        "successes": success,
        "failures": failure,
        "success_rate": success_rate,
        "total": total,
        "average": average,
        "rate_of_profitability": rate_of_profitability
    }

def run_universe(probability: float, reward: float, penalty: float, simulations_per_universe: int) -> int:
    balance = 0

    for _ in range(simulations_per_universe):
        if(is_success(probability)):
            balance += reward
        else:
            balance += penalty

    return balance

def universe_simulator(probability: float, reward: float, penalty: float, number_of_universes: int,simulations_per_universe: int) -> dict:
    final_balances = []
    balance = 0

    for _ in range (number_of_universes):
        balance = run_universe(probability, reward, penalty, simulations_per_universe)
        final_balances.append(balance)

    average_final_balance = sum(final_balances) / number_of_universes
    profitable_universes = sum(1 for b in final_balances if b > 0)

    return {
        "average_final_balance": average_final_balance,
        "probability_of_profit": profitable_universes / number_of_universes,
        "best_universe": max(final_balances),
        "worst_universe": min(final_balances)
    }

if __name__ == "__main__":
    result = universe_simulator(0.95, 0.80, -80, 1000, 1000)
    print(result)



