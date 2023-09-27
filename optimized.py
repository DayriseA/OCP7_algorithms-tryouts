"""
Adaptation of the 0-1 knapsack problem for our bond portfolio optimization.
Using dynamic programming to solve the problem.
"""

import csv
import time


class Bond:
    def __init__(self, name, price, yield_):
        self.name = name
        self.price = price
        self.yield_ = yield_
        self.profit = price * yield_ / 100


def timer(func):
    """Decorator to measure the execution time of a function."""

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function '{func.__name__}' took {end - start:.2f} seconds to execute.")
        return result

    return wrapper


@timer
def find_optimal_combination(bonds, funds):
    """
    Dynamic programming function for the best bonds combination within the given funds.
    Args:
        bonds (list): list of Bond objects
        funds (int): amount of funds available

    Returns:
        tuple: (best_combination, best_profit)
    """
    num_bonds = len(bonds)
    # Set a matrix to store maximum profit for each subproblem, initialized with zeros.
    # dp[i][j] represents the maximum profit for the first i bonds with j funds.
    dp = [[0 for _ in range(funds + 1)] for _ in range(num_bonds + 1)]

    for i in range(1, num_bonds + 1):
        for j in range(funds + 1):
            bond = bonds[i - 1]  # 0-indexed, so current bond is i-1
            if bond.price <= j:
                # Two options:

                # 1) Include the current bond: add its profit to the maximum profit
                # obtained with the previous bonds and remaining funds
                profit_included = bond.profit + dp[i - 1][j - bond.price]

                # 2) Exclude the current bond: maximum profit obtained with the
                # previous bonds without considering the current bond
                profit_excluded = dp[i - 1][j]

                # Take the maximum of the two options and store it to dp[i][j]
                dp[i][j] = max(profit_included, profit_excluded)
            else:
                # Current bond excluded due to funds constraint
                dp[i][j] = dp[i - 1][j]

    # Backtrack to find the bonds included in the optimal combination
    best_combination = []
    i = num_bonds
    j = funds
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            best_combination.append(bonds[i - 1])
            j -= bonds[i - 1].price
        i -= 1

    best_profit = dp[num_bonds][funds]

    return best_combination, best_profit


def main():
    bonds = []
    funds = 500
    bonds_path = "data/bonds_list.csv"

    # Get bonds from the CSV file
    with open(bonds_path, mode="r", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            bond = Bond(row["Bonds"], int(row["Price"]), int(row["Yield"]))
            bonds.append(bond)

    best_combination, best_profit = find_optimal_combination(bonds, funds)
    best_combination_cost = sum([bond.price for bond in best_combination])
    print("Best combination: ", [bond.name for bond in best_combination[::-1]])
    print(f"Associated profit: {best_profit:.2f} €")
    print(f"Total price: {best_combination_cost} €\n")


if __name__ == "__main__":
    main()
