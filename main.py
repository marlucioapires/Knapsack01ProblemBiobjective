# -*- coding: utf-8 -*-
from algorithms import solve_knapsack01_problem
from constants import Const, StrConst
from file_functions import processate_instance_file
from knapsack01_biobjective_instance import Knapsack01BiobjectiveSolution
import sys
from typing import Dict, List
from algorithms import *
import random
from general_functions import sort_solutions
import matplotlib.pyplot as plt
import numpy as np


def plot_graphic_of_solutions(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution],
        list_of_non_dominated_solutions: List[int]) -> None:
    is_non_dominated_solution = [0] * len(sorted_list_of_solutions)
    for i in list_of_non_dominated_solutions:
        is_non_dominated_solution[i] = 1
    plt.plot([sorted_list_of_solutions[i].profit()
              for i in range(len(sorted_list_of_solutions))
              if is_non_dominated_solution[i]],
             [sorted_list_of_solutions[i].weight()
              for i in range(len(sorted_list_of_solutions))
              if is_non_dominated_solution[i]], 'b+')
    plt.plot([sorted_list_of_solutions[i].profit()
              for i in range(len(sorted_list_of_solutions))
              if not is_non_dominated_solution[i]],
             [sorted_list_of_solutions[i].weight()
              for i in range(len(sorted_list_of_solutions))
              if not is_non_dominated_solution[i]], 'r+')
    # plt.axis([0, 6, 0, 20])
    plt.xlabel('LUCRO')
    plt.ylabel('PESO')
    plt.title('Problema da Mochila 0-1 Biobjetivo')
    plt.show()


def print_profit_and_weight_of_solutions(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]) -> None:
    print("VALORES DAS FUNCOES:")
    print("LUCRO / PESO")
    for solution in sorted_list_of_solutions:
        print(solution.profit(), solution.weight())


def print_profit_and_weight_of_solutions_with_nd_information(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution],
        list_of_non_dominated_solutions: List[int]) -> None:
    print("VALORES DAS FUNCOES:")
    print("LUCRO / PESO")
    j_aux = 0
    for i, solution in enumerate(sorted_list_of_solutions):
        str_nd_aux = ""
        if j_aux < len(list_of_non_dominated_solutions) and \
                i == list_of_non_dominated_solutions[j_aux]:
            j_aux += 1
            str_nd_aux = "ND"
        print(solution.profit(), solution.weight(), str_nd_aux)


def processate_line_command_parameters(list_of_params: List[str]) -> Dict:
    dict_of_params = {}
    error = False
    iter_param = 1
    dict_of_params[Const.INSTANCE_NUMBER_INSIDE_FILE] = 1
    while iter_param < len(list_of_params):
        if list_of_params[iter_param].lower() == \
                StrConst.LINE_COMMAND_PARAM_INSTANCE_NUMBER_INSIDE_FILE.value:
            try:
                dict_of_params[Const.INSTANCE_NUMBER_INSIDE_FILE] = \
                    int(list_of_params[(iter_param + 1)])
                iter_param += 2
                continue
            except (IndexError, ValueError):
                error = True
                break
        if not dict_of_params.get(Const.INSTANCE_FILE):
            dict_of_params[Const.INSTANCE_FILE] = list_of_params[iter_param]
        elif not dict_of_params.get(Const.OUTPUT_FILE):
            dict_of_params[Const.OUTPUT_FILE] = list_of_params[iter_param]
        iter_param += 1
    if error or len(list_of_params) == 1 or not dict_of_params.get(Const.INSTANCE_FILE):
        print("Erro na passagem de parametros via linha de comando!")
        return {}
    if not dict_of_params.get(Const.INSTANCE_NUMBER_INSIDE_FILE):
        dict_of_params[Const.INSTANCE_NUMBER_INSIDE_FILE] = 1
    return dict_of_params


def main():
    random.seed()
    dict_of_params = processate_line_command_parameters(sys.argv)
    # print(dict_of_params)
    if dict_of_params:
        kp_instance = processate_instance_file(
            dict_of_params[Const.INSTANCE_FILE], dict_of_params[Const.INSTANCE_NUMBER_INSIDE_FILE])
        if kp_instance:
            list_of_solutions = []
            for i in range(10000):
                list_of_solutions.append(
                    generate_ramdomic_solution_for_knapsack_01_problem(kp_instance))
            sort_solutions(list_of_solutions)
            list_of_non_dominated_solutions = \
                calculate_list_of_non_dominated_solutions(list_of_solutions)
            print_profit_and_weight_of_solutions_with_nd_information(
                list_of_solutions, list_of_non_dominated_solutions)
            # print_profit_and_weight_of_solutions(list_of_solutions)
            print("SOLUCOES NAO DOMINADAS:")
            print(calculate_list_of_non_dominated_solutions(list_of_solutions))
            plot_graphic_of_solutions(list_of_solutions, list_of_non_dominated_solutions)


if __name__ == "__main__":
    main()
    sys.exit(0)
