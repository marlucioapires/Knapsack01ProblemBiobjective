# -*- coding: utf-8 -*-
from general_functions import sort_solutions
from knapsack01_biobjective_instance import Knapsack01BiobjectiveInstance
from knapsack01_biobjective_instance import Knapsack01BiobjectiveSolution
from typing import List, Tuple
import random
import time
import math


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


def is_non_dominated_with_sorted_solutions(
        solution1: Knapsack01BiobjectiveSolution, solution2: Knapsack01BiobjectiveSolution
) -> bool:
    if solution1.weight() < solution2.weight():
        return True
    return False


def calculate_list_of_indexes_of_non_dominated_solutions(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]) -> List[int]:
    if not sorted_list_of_solutions:
        return []
    list_of_non_dominated_solutions = [0]  # A primeira solução da lista é não dominada.
    # profit_of_last_nd = sorted_list_of_solutions[0].profit()
    weight_of_last_nd = sorted_list_of_solutions[0].weight()

    # Percorre-se as demais soluções da lista e contabiliza-se as demais soluções não dominadas.
    for i, solution in enumerate(list(sorted_list_of_solutions)[1:]):
        if solution.weight() < weight_of_last_nd:
            # profit_of_last_nd = solution.profit()
            weight_of_last_nd = solution.weight()
            list_of_non_dominated_solutions.append(i + 1)
        # elif solution.weight() == weight_of_last_nd and solution.profit() == profit_of_last_nd:
        #     list_of_non_dominated_solutions.append(i + 1)
    return list_of_non_dominated_solutions


def generate_ramdomic_solution_for_knapsack_01_problem_only_valid(
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


def generate_ramdomic_solution_for_knapsack_01_problem(
        kp01_instance: Knapsack01BiobjectiveInstance) -> Knapsack01BiobjectiveSolution:
    kp01_solution = Knapsack01BiobjectiveSolution(kp01_instance)
    indirect_index_of_items = list(range(kp01_instance.n))
    random.shuffle(indirect_index_of_items)
    for item_iter in range(kp01_instance.n):
        if random.randint(0, 1):
            kp01_solution.x_vector[indirect_index_of_items[item_iter]] = 1
    kp01_solution.update_weight_and_profit()
    return kp01_solution


def generate_list_of_ramdomic_solution_for_knapsack_01_problem(
        kp01_instance: Knapsack01BiobjectiveInstance,
        nr_of_solutions: int
) -> List[Knapsack01BiobjectiveSolution]:
    list_of_solutions = []
    for i in range(nr_of_solutions):
        list_of_solutions.append(
            generate_ramdomic_solution_for_knapsack_01_problem(kp01_instance))
    return list_of_solutions


def generate_solution_with_single_item_for_knapsack_01_problem(
        kp01_instance: Knapsack01BiobjectiveInstance, item: int) -> Knapsack01BiobjectiveSolution:
    kp01_solution = Knapsack01BiobjectiveSolution(kp01_instance)
    if kp01_instance.weight[item] <= kp01_instance.c:
        kp01_solution.x_vector[item] = 1
    kp01_solution.update_weight_and_profit()
    return kp01_solution


def generate_list_of_solutions_with_single_items_for_knapsack_01_problem(
        kp01_instance: Knapsack01BiobjectiveInstance) -> List[Knapsack01BiobjectiveSolution]:
    list_of_solutions = []
    for i in range(kp01_instance.n):
        solution = generate_solution_with_single_item_for_knapsack_01_problem(kp01_instance, i)
        if solution.weight() >= 0:
            list_of_solutions.append(solution)
    return list_of_solutions


def delete_dominated_solutions_from_sorted_list(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]):
    list_of_indexes_of_non_dominated_solutions = \
        calculate_list_of_indexes_of_non_dominated_solutions(sorted_list_of_solutions)
    is_non_dominated_solution = [0] * len(sorted_list_of_solutions)
    for i in list_of_indexes_of_non_dominated_solutions:
        is_non_dominated_solution[i] = 1
    i = 0
    while i < len(sorted_list_of_solutions):
        if not is_non_dominated_solution[i]:
            del sorted_list_of_solutions[i]
            del is_non_dominated_solution[i]
        else:
            i += 1


def branch_and_bound_for_knapsack_01_problem_biobjective(
        kp01_instance: Knapsack01BiobjectiveInstance,
        max_execution_time: float = math.inf) -> Tuple[int, List[Knapsack01BiobjectiveSolution]]:
    execution_start_time = time.time()
    solution_zero = Knapsack01BiobjectiveSolution(kp01_instance)
    list_of_non_dominated_solutions = [solution_zero, ]
    count_solutions_generated = 1
    for item_iter in range(kp01_instance.n):
        print("RAMIFICACAO DO ITEM NR. %d / %d" % (item_iter + 1, kp01_instance.n))
        list_of_new_solutions = []
        for solution_iter in list_of_non_dominated_solutions:
            count_solutions_generated += 1
            new_solution = Knapsack01BiobjectiveSolution(kp01_instance)
            new_solution.x_vector = list(solution_iter.x_vector)
            new_solution.x_vector[item_iter] = 1
            list_of_new_solutions.append(new_solution)
        list_of_non_dominated_solutions.extend(list_of_new_solutions)
        sort_solutions(list_of_non_dominated_solutions)
        delete_dominated_solutions_from_sorted_list(list_of_non_dominated_solutions)
        if max_execution_time != math.inf:
            execution_current_time = (time.time() - execution_start_time)
            if execution_current_time > max_execution_time:
                break
    print("TOTAL DE SOLUCOES GERADAS NO BRANCH AND BOUND: %d" % count_solutions_generated)
    return count_solutions_generated, list_of_non_dominated_solutions
