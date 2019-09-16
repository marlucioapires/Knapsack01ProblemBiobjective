# -*- coding: utf-8 -*-
# from algorithms import solve_knapsack01_problem
from constants import Const, StrConst
from file_functions import processate_instance_file
from knapsack01_biobjective_instance import Knapsack01BiobjectiveSolution
from copy import deepcopy
import sys
from typing import Dict
from algorithms import *
import random
from general_functions import sort_solutions
import matplotlib.pyplot as plt
# import numpy as np


def plot_graphic_of_solutions(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution],
        list_of_non_dominated_solutions: List[int],
        optimal_solution: Knapsack01BiobjectiveSolution = None) -> None:
    is_non_dominated_solution = [0] * len(sorted_list_of_solutions)
    for i in list_of_non_dominated_solutions:
        is_non_dominated_solution[i] = 1
    plt.plot([sorted_list_of_solutions[i].profit()
              for i in range(len(sorted_list_of_solutions))
              if is_non_dominated_solution[i]],
             [sorted_list_of_solutions[i].weight()
              for i in range(len(sorted_list_of_solutions))
              if is_non_dominated_solution[i]], 'bo')
    plt.plot([sorted_list_of_solutions[i].profit()
              for i in range(len(sorted_list_of_solutions))
              if not is_non_dominated_solution[i]],
             [sorted_list_of_solutions[i].weight()
              for i in range(len(sorted_list_of_solutions))
              if not is_non_dominated_solution[i]], 'r+')
    if optimal_solution:
        plt.plot([optimal_solution.profit()],
                 [optimal_solution.weight()], 'ro')
    # plt.axis([0, 6, 0, 20])
    plt.xlabel('LUCRO')
    plt.ylabel('PESO')
    plt.title('Problema da Mochila 0-1 Biobjetivo')
    plt.show()


def print_profit_and_weight_of_solutions(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution]) -> None:
    print("\nVALORES DAS FUNCOES:")
    print("LUCRO / PESO")
    for solution in sorted_list_of_solutions:
        print(solution.profit(), solution.weight())


def print_profit_and_weight_of_solutions_with_nd_information(
        sorted_list_of_solutions: List[Knapsack01BiobjectiveSolution],
        list_of_non_dominated_solutions: List[int]) -> None:
    print("\nVALORES DAS FUNCOES:")
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
    dict_of_params[Const.NUMBER_OF_RANDOMIC_SOLUTIONS] = 0
    dict_of_params[Const.EXECUTION_TIME] = math.inf
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
        if list_of_params[iter_param].lower() == \
                StrConst.LINE_COMMAND_PARAM_NUMBER_OF_RANDOMIC_SOLUTIONS.value:
            try:
                dict_of_params[Const.NUMBER_OF_RANDOMIC_SOLUTIONS] = \
                    int(list_of_params[(iter_param + 1)])
                iter_param += 2
                continue
            except (IndexError, ValueError):
                error = True
                break
        if list_of_params[iter_param].lower() == \
                StrConst.LINE_COMMAND_PARAM_EXECUTION_TIME.value:
            try:
                dict_of_params[Const.EXECUTION_TIME] = \
                    float(list_of_params[(iter_param + 1)])
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
    start_time = time.time()
    random.seed()
    dict_of_params = processate_line_command_parameters(sys.argv)
    if dict_of_params:
        kp_instance = processate_instance_file(
            dict_of_params[Const.INSTANCE_FILE], dict_of_params[Const.INSTANCE_NUMBER_INSIDE_FILE])
        if kp_instance:
            print("NOME INSTANCIA: %s" % kp_instance.name)
            list_of_solutions = []

            # solve_knapsack01_problem(kp_instance)
            solution_optimal = Knapsack01BiobjectiveSolution(kp_instance)
            solution_optimal.x_vector = deepcopy(kp_instance.x_vector)
            solution_optimal.update_weight_and_profit()
            # list_of_solutions.append(solution_optimal)

            # list_of_solutions.extend(
            #     generate_list_of_solutions_with_single_items_for_knapsack_01_problem(kp_instance))

            # Geração de soluções randômicas:
            # if dict_of_params[Const.NUMBER_OF_RANDOMIC_SOLUTIONS]:
            #     print("GERANDO SOLUCOES RANDOMICAS (TOTAL: %d)..." %
            #           dict_of_params[Const.NUMBER_OF_RANDOMIC_SOLUTIONS])
            #     for i in range(dict_of_params[Const.NUMBER_OF_RANDOMIC_SOLUTIONS]):
            #         list_of_solutions.append(
            #             generate_ramdomic_solution_for_knapsack_01_problem(kp_instance))
            #     print("FIM DA GERACAO DE SOLUCOES RANDOMICAS")

            # sort_solutions(list_of_solutions)
            # list_of_non_dominated_solutions = \
            #     calculate_list_of_indexes_of_non_dominated_solutions(list_of_solutions)

            print("INICIANDO BRANCH AND BOUND...")
            nr_solutions_generated, list_of_solutions = \
                branch_and_bound_for_knapsack_01_problem_biobjective(
                    kp_instance, dict_of_params[Const.EXECUTION_TIME])
            print("FIM DO BRANCH AND BOUND")
            # list_of_solutions.append(solution_optimal)
            # sort_solutions(list_of_solutions)

            list_of_non_dominated_solutions = \
                calculate_list_of_indexes_of_non_dominated_solutions(list_of_solutions)

            print_profit_and_weight_of_solutions_with_nd_information(
                list_of_solutions, list_of_non_dominated_solutions)
            # print_profit_and_weight_of_solutions(list_of_solutions)
            # print("\nSOLUCOES NAO DOMINADAS:")
            # print([i + 1 for i in list_of_non_dominated_solutions])
            print("\nTOTAL DE SOLUCOES GERADAS NO BRANCH AND BOUND: %d" % nr_solutions_generated)
            print("\nNUMERO DE SOLUCOES NAO DOMINADAS: %d" % len(list_of_non_dominated_solutions))
            end_time = (time.time() - start_time)
            print("\n--- TEMPO TOTAL DE EXECUCAO: %s segundos ---" % round(end_time, 3))
            plot_graphic_of_solutions(list_of_solutions, list_of_non_dominated_solutions, solution_optimal)
            # plot_graphic_of_solutions(list_of_solutions, list_of_non_dominated_solutions)


if __name__ == "__main__":
    main()
    sys.exit(0)
