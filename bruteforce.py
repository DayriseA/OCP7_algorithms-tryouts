"""
Bruteforce algorithm for bond portfolio optimization.
A merely adaptation of the knapsack problem.
We will not discuss the solution of nested loops because for 20 elements it would be 
really horrible to write, and O(20^20) seems like a pretty bad idea to try.
"""

import csv
import itertools
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
def bruteforce_w_itertools(bonds, funds):
    """
    Takes a list of bonds and amount of funds available. A bond can be bought only once.
    Returns the optimal bonds combination and profit.
    """
    best_combination = []
    best_profit = 0
    best_combination_price = 0

    for i in range(1, len(bonds) + 1):
        for combination in itertools.combinations(bonds, i):
            total_price = sum([bond.price for bond in combination])
            total_profit = sum([bond.profit for bond in combination])

            if total_price <= funds and total_profit > best_profit:
                best_combination = combination
                best_profit = total_profit
                best_combination_price = total_price

    return best_combination, best_profit, best_combination_price


def generate_combinations(bonds):
    """
    Takes a list and returns all possible combinations of its elements.
    Combinations are combined with total price and profit in the form of a tuple.
    Not using itertools but bitmasking instead.
    """
    # Will be used for the solution without itertools
    n = len(bonds)
    combinations = []

    for i in range(1, 2**n):
        current_combination = []
        total_price = 0
        total_profit = 0

        for j in range(n):
            if (i >> j) & 1:
                bond = bonds[j]
                current_combination.append(bond)
                total_price += bond.price
                total_profit += bond.profit

        combinations.append((current_combination, total_price, total_profit))

    return combinations


@timer
def bruteforce_wo_itertools(bonds, funds):
    """
    Takes a list of bonds and amount of funds available. A bond can be bought only once.
    Returns the optimal bonds combination and profit.
    Not using itertools.
    """
    best_combination = []
    best_profit = 0
    best_combination_price = 0

    combinations = generate_combinations(bonds)

    for combination, total_price, total_profit in combinations:
        if total_price <= funds and total_profit > best_profit:
            best_combination = combination
            best_profit = total_profit
            best_combination_price = total_price

    return best_combination, best_profit, best_combination_price


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

    best_combination, best_profit, total_price = bruteforce_w_itertools(bonds, funds)
    print("Best combination: ", [bond.name for bond in best_combination])
    print(f"Associated profit: {best_profit:.2f} €")
    print(f"Total price: {total_price} €\n")

    best_combination, best_profit, total_price = bruteforce_wo_itertools(bonds, funds)
    print("Best combination: ", [bond.name for bond in best_combination])
    print(f"Associated profit: {best_profit:.2f} €")
    print(f"Total price: {total_price} €")


if __name__ == "__main__":
    main()
