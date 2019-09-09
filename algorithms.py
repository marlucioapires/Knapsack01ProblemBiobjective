# -*- coding: utf-8 -*-
from knapsack01_biobjective_instance import Knapsack01BiobjectiveInstance


def knapsack_01_problem_with_dynamic_programming(kp01_instance: Knapsack01BiobjectiveInstance) -> int:
    array_memo = {}
    for i in range(1, kp01_instance.n + 1):
        array_memo[i, 0] = 0
    for w in range(0, kp01_instance.c + 1):
        array_memo[0, w] = 0
    for i in range(1, kp01_instance.n + 1):
        for w in range(1, kp01_instance.c + 1):
            if kp01_instance.weight[i - 1] > w:
                array_memo[i, w] = array_memo[i - 1, w]
            else:
                array_memo[i, w] = \
                    max(array_memo[i - 1, w],
                        array_memo[i - 1, w - kp01_instance.weight[i - 1]] + kp01_instance.profit[i - 1])
    return array_memo[kp01_instance.n, kp01_instance.c]


def solve_knapsack01_problem(kp01_instance: Knapsack01BiobjectiveInstance) -> int:
    return knapsack_01_problem_with_dynamic_programming(kp01_instance)
