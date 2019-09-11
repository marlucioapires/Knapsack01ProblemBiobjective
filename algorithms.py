# -*- coding: utf-8 -*-
from knapsack01_biobjective_instance import Knapsack01BiobjectiveInstance
from knapsack01_biobjective_instance import Knapsack01BiobjectiveSolution
from typing import List, Tuple
import random


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


def apply_movement_put_or_remove_item(
        kp01_solution: Knapsack01BiobjectiveSolution, position: int) -> Tuple[int, int]:
    return kp01_solution.update_x_vector(position, (kp01_solution.x_vector[position] + 1) % 2)


def apply_movement_put_or_remove_item_in_randomic_position(
        kp01_solution: Knapsack01BiobjectiveSolution) -> Tuple[int, int]:
    position = random.randrange(kp01_solution.kp_instance.n)
    return apply_movement_put_or_remove_item(kp01_solution, position)


def calculate_position_in_pool_of_solutions(
        kp01_solution: Knapsack01BiobjectiveSolution,
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]) -> Tuple[bool, int]:
    position_to_return = -1
    non_dominated = True
    for position, solution in reversed(list(enumerate(sorted_list_of_solutions))):
        if solution.profit() > kp01_solution.profit() or \
                (solution.profit() == kp01_solution.profit() and
                 solution.weight() <= kp01_solution.weight()):
            position_to_return = position
            break
    for i in range(position_to_return, -1, -1):
        if sorted_list_of_solutions[i].weight() < kp01_solution.weight() or \
                (sorted_list_of_solutions[i].weight() == kp01_solution.weight() and
                 sorted_list_of_solutions[i].profit() != kp01_solution.profit()):
            non_dominated = False
    return non_dominated, position_to_return + 1


def calculate_list_of_non_dominated_solutions(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]) -> List[int]:
    list_of_non_dominated_solutions = [0]
    profit_of_last_nd = sorted_list_of_solutions[0].profit()
    weight_of_last_nd = sorted_list_of_solutions[0].weight()
    for i, solution in enumerate(list(sorted_list_of_solutions)[1:]):
        if solution.weight() < weight_of_last_nd:
            profit_of_last_nd = solution.profit()
            weight_of_last_nd = solution.weight()
            list_of_non_dominated_solutions.append(i + 1)
        elif solution.weight() == weight_of_last_nd and solution.profit() == profit_of_last_nd:
            list_of_non_dominated_solutions.append(i + 1)
    return list_of_non_dominated_solutions


def generate_ramdomic_solution_for_knapsack_01_problem(
        kp01_instance: Knapsack01BiobjectiveInstance) -> Knapsack01BiobjectiveSolution:
    kp01_solution = Knapsack01BiobjectiveSolution(kp01_instance)
    weight_sum = 0
    indirect_index_of_items = list(range(kp01_instance.n))
    random.shuffle(indirect_index_of_items)
    for item_iter in range(kp01_instance.n):
        put_item_in_knapsack = random.randint(0, 1)
        if put_item_in_knapsack and \
                weight_sum + kp01_instance.weight[indirect_index_of_items[item_iter]] <= kp01_instance.c:
            kp01_solution.x_vector[indirect_index_of_items[item_iter]] = 1
            weight_sum += kp01_instance.weight[indirect_index_of_items[item_iter]]
        elif weight_sum == kp01_instance.c:
            break
    kp01_solution.update_weight_and_profit()
    return kp01_solution
