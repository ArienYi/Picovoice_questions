from typing import Sequence
import random
'''
Question 1: The probability of rain on a given calendar day in Vancouver is p[i], where i is the day's index.
For example, p[0] is the probability of rain on January 1st , and p[10] is the probability of precipitation on 
January 11th. Assume the year has 365 days (i.e., p has 365 elements). What is the chance it rains more than 
n (e.g., 100) days in Vancouver? Write a function that accepts p (probabilities of rain on a given calendar day) 
and n as input arguments and returns the possibility of raining at least n days.
'''

'''
Dynamic Programming Approach
Time Complexity: O(num_of_days^2)
Space Complexity: O(num_of_days^2)
'''
def prob_rain_more_than_n_dp(p: Sequence[float], n: int) -> float:
    num_of_days = len(p)
    # initialize the dp table
    # dp[i][j] stores the probability of having exactly j rainy days in the first i days.
    dp = [[0.0] * (num_of_days + 1) for _ in range(num_of_days + 1)]

    # base
    dp[0][0] = float(1)

    # fill the dp table
    for i in range(1, num_of_days + 1):
        for j in range(num_of_days + 1):

            # case of the day i is not rainy
            # number of rainy day j stays the same with i-1
            dp[i][j] = dp[i - 1][j] * (1 - p[i - 1])
            if j > 0:

                # case of the day i is rainy
                # number of rainy day becomes j, so we use j-1 among the first i-1 days
                dp[i][j] += dp[i - 1][j - 1] * p[i - 1]

    # Sum probabilities for more than n rainy days
    res = sum(dp[num_of_days][j] for j in range(n + 1, num_of_days))
    return res

'''
Monte Carlo Approach
Time Complexity: O(num_simulations * num_of_days)
Space Complexity: O(1)
'''
def prob_rain_more_than_n_monte_carlo(p: Sequence[float], n: int, num_of_simulations: int = 1e5) -> float:
    num_of_days = len(p)
    # Count how many simulations end up with > n rainy days
    counter = 0

    for _ in range(num_of_simulations):
        # number of rainy days in one simulation
        num_of_rainy = 0
        for day in range(num_of_days):
            # generate a float within [0,1)
            # if that float falls between [0, p[day]), we claim that day is rainy
            if random.random() <= p[day]:
                num_of_rainy += 1
        if num_of_rainy > n:
            counter += 1

    # The estimate is how many simulations had > n rainy days, divided by total simulations
    return counter / num_of_simulations

'''
DP approach will provide the accurate solution for the problem, while Monte Carlo Approach provides an approximation.
However, the later one will be closer and closer to the ground truth with higher num_of_simulations.
Meanwhile, it introduces O(1) space complexity, which is much better than DP approach.
'''