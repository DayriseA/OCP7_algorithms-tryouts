"""
Bruteforce algorithm for bond portfolio optimization.
A merely adaptation of the knapsack problem.
We will not discuss the solution of nested loops because for 20 elements it would be 
really horrible to write, and O(20^20) seems like a pretty bad idea to try.
"""

import csv
import itertools


class Bond:
    def __init__(self, name, price, yield_):
        self.name = name
        self.price = price
        self.yield_ = yield_
        self.profit = price * yield_ / 100


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

    # for bond in bonds:
    #     print(f"{bond.name} - {bond.price} - {bond.yield_} - {bond.profit}")

    best_combination, best_profit, total_price = bruteforce_w_itertools(bonds, funds)

    print("Best combination: ", [bond.name for bond in best_combination])
    print(f"Associated profit: {best_profit:.2f} €")
    print(f"Total price: {total_price} €")


if __name__ == "__main__":
    main()
