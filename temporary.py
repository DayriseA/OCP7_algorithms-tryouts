def knapsack(max_weight, weights, values, num_items):
    """
    Dynamic programming function for the 0-1 knapsack problem.
    Args:
        max_weight (int): maximum weight the knapsack can hold
        weights (list): list of weights of each item
        values (list): list of values of each item
        num_items (int): number of items

    Returns:
        int: maximum value that can be put in the knapsack
    """
    # initialize the matrix with zeros
    K = [[0 for _ in range(max_weight + 1)] for _ in range(num_items + 1)]

    # K[i][w] represents the maximum value obtainable using the first 'i' items
    # and a knapsack of maximum weight capacity of 'w'
    for i in range(num_items + 1):
        for w in range(max_weight + 1):
            # base case: no items or knapsack of capacity 0
            if i == 0 or w == 0:
                K[i][w] = 0
            # 0-indexed arrays so current item is i-1
            elif weights[i - 1] <= w:
                # two options:

                # 1) include the current item: add its value to the maximum value
                # obtained with the previous items and remaining capacity
                value_item_included = values[i - 1] + K[i - 1][w - weights[i - 1]]

                # 2) exclude the current item: maximum value obtained with the
                # previous items without considering the current item
                value_item_excluded = K[i - 1][w]

                # Take the maximum of the two options and store it to K[i][w]
                K[i][w] = max(value_item_included, value_item_excluded)
            else:
                K[i][w] = K[i - 1][w]

    return K[num_items][max_weight]
