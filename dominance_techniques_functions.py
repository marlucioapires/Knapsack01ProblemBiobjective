# -*- coding: utf-8 -*-
from typing import Dict, List
from knapsack01_biobjective_instance import Knapsack01BiobjectiveSolution
from algorithms import calculate_list_of_indexes_of_non_dominated_solutions, is_non_dominated_with_sorted_solutions
from itertools import combinations


def calculate_dominance_depth(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]) -> List[List[Knapsack01BiobjectiveSolution]]:
    list_of_solutions_not_processsed = list(range(len(sorted_list_of_solutions)))
    list_of_front_solutions_by_dominance_depth = []
    while list_of_solutions_not_processsed:
        list_of_solutions = [sorted_list_of_solutions[i] for i in list_of_solutions_not_processsed]
        front = calculate_list_of_indexes_of_non_dominated_solutions(list_of_solutions)
        list_of_front_solutions_by_dominance_depth.append([list_of_solutions[i] for i in front])
        for i in reversed(range(len(front))):
            del list_of_solutions_not_processsed[front[i]]
    return list_of_front_solutions_by_dominance_depth


def calculate_dominance_rank(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]
) -> List[int]:
    list_of_rank = [0] * len(sorted_list_of_solutions)
    for i, j in list(combinations(range(len(sorted_list_of_solutions)), 2)):
        if is_non_dominated_with_sorted_solutions(sorted_list_of_solutions[i], sorted_list_of_solutions[j]):
            list_of_rank[j] += 1
    return list_of_rank


def calculate_dominance_count(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]
) -> List[int]:
    list_of_rank = [0] * len(sorted_list_of_solutions)
    for i, j in list(combinations(range(len(sorted_list_of_solutions)), 2)):
        if is_non_dominated_with_sorted_solutions(sorted_list_of_solutions[i], sorted_list_of_solutions[j]):
            list_of_rank[i] += 1
    return list_of_rank


# def print_profit_and_weight_of_solutions_with_nd_information_v2(
#         sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution],
#         list_of_non_dominated_solutions: List[int]) -> None:
#     print("\nVALORES DAS FUNCOES:")
#     print("LUCRO / PESO")
#     j_aux = 0
#     for i, solution in enumerate(sorted_list_of_solutions):
#         str_nd_aux = ""
#         if j_aux < len(list_of_non_dominated_solutions) and \
#                 i == list_of_non_dominated_solutions[j_aux]:
#             j_aux += 1
#             str_nd_aux = "ND"
#         print(solution.profit(), solution.weight(), str_nd_aux)


# def calculate_dominance_depth(
#         sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]) -> List[List[Knapsack01BiobjectiveSolution]]:
#     list_of_solutions = deepcopy(sorted_list_of_solutions)
#     list_of_indexes_of_solutions_by_dominance_depth = []
#     while list_of_solutions:
#         front = calculate_list_of_indexes_of_non_dominated_solutions(list_of_solutions)
#         list_of_indexes_of_solutions_by_dominance_depth.append([deepcopy(list_of_solutions[i]) for i in front])
#         for i in reversed(range(len(front))):
#             del list_of_solutions[front[i]]
#     return list_of_indexes_of_solutions_by_dominance_depth
