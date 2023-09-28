"""Extract historical data from local file and use our algorithms for backtesting."""

import csv
from optimized import find_optimal_combination


class Asset:
    def __init__(self, name, price, yield_) -> None:
        self.name = name
        self.price = round(price)
        self.price_difference = price - self.price
        self.yield_ = yield_
        self.profit = price * yield_ / 100

    def __str__(self) -> str:
        exact_price = self.price + self.price_difference
        return (
            f"{self.name} - {exact_price:.2f}€ - "
            f"{self.profit:.2f}% yield (for 2 years)"
        )


def get_assets_from_csv(path):
    """
    Get assets from a CSV file. Ignore lines with missing or incorrect data.
    Args:
        path (str): path to the CSV file
    Returns:
        assets (list): list of Asset objects
    """
    assets = []
    with open(path, mode="r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 3 or not all(row[0:3]) or float(row[1]) <= 0:
                # Ignore missing data or non-positive prices
                continue
            asset = Asset(row[0], float(row[1]), float(row[2]))
            assets.append(asset)
    return assets


def main():
    sienna_assets_1 = get_assets_from_csv("data/dataset1_Sienna.csv")
    sienna_assets_2 = get_assets_from_csv("data/dataset2_Sienna.csv")
    funds = 500

    best_combination, best_profit = find_optimal_combination(sienna_assets_1, funds)
    best_combination_cost = sum(
        [(asset.price + asset.price_difference) for asset in best_combination]
    )
    print("\nAssets bought from Sienna's dataset 1:")
    for asset in best_combination[::-1]:
        print(asset)
    print(
        f"\n => Associated profit: {best_profit:.2f} €"
        f"\n =>Total cost: {best_combination_cost:.2f} €\n"
    )

    best_combination, best_profit = find_optimal_combination(sienna_assets_2, funds)
    best_combination_cost = sum(
        [(asset.price + asset.price_difference) for asset in best_combination]
    )
    print("\nAssets bought from Sienna's dataset 2:")
    for asset in best_combination[::-1]:
        print(asset)
    print(
        f"\n => Associated profit: {best_profit:.2f} €"
        f"\n =>Total cost: {best_combination_cost:.2f} €\n"
    )


if __name__ == "__main__":
    main()
