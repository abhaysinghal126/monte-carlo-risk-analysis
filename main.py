import random

def is_success(probability: float) -> bool:
    if not 0 <= probability <= 1:
        raise ValueError("Probablity must be between 0 and 1.")
    return random.random() < probability

def simulator(probability: float, reward: float, penalty: float, number_of_simulations: int) -> dict:

    if not type(number_of_simulations) == int:
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

if __name__ == "__main__":
    result = simulator(0.3, 100, -40, 1000000)
    print(result)



