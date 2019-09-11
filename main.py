# -*- coding: utf-8 -*-
from algorithms import solve_knapsack01_problem
from constants import Const, StrConst
from file_functions import processate_instance_file
from knapsack01_biobjective_instance import Knapsack01BiobjectiveSolution
import sys
from typing import Dict, List
from algorithms import *
import random
from copy import deepcopy


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
            # print(str(kp_instance))
            # solution = solve_knapsack01_problem(kp_instance)
            # print("SOLUCAO OTIMA: %d" % solution)
            # solution_is_valid = False
            # if kp_instance.z == solution:
            #     solution_is_valid = True
            # print("SOLUCAO EH VALIDA? R: %s" % str(solution_is_valid))
            # solution = Knapsack01BiobjectiveSolution(kp_instance)
            # solution.x_vector = list(kp_instance.x_vector)
            # print("\nCLASSE SOLUTION:")
            # print(str(solution))
            # solution = generate_ramdomic_solution_for_knapsack_01_problem(kp_instance)
            # print("\nSOLUCAO GERADA ALEATORIAMENTE:")
            # print(str(solution))
            # print("SOLUCAO EH VALIDA? R: " + str(solution.is_valid()))
            # print("APLICANDO MOVIMENTO NA SOLUCAO...")
            # apply_movement_put_or_remove_item_in_randomic_position(solution)
            # print("\nSOLUCAO APOS ALTERACAO:")
            # print(str(solution))
            # print("SOLUCAO EH VALIDA? R: " + str(solution.is_valid()))
            # print("LUCRO DA SOLUCAO: %d" % solution.profit())
            # print("PESO DA SOLUCAO: %d" % solution.weight())

            list_of_sorted_solutions = []
            for i in range(100):
                solution = generate_ramdomic_solution_for_knapsack_01_problem(kp_instance)
                non_dominated, pos = \
                    calculate_position_in_pool_of_solutions(solution, list_of_sorted_solutions)
                list_of_sorted_solutions.insert(pos, deepcopy(solution))
            list_of_non_dominated_solutions = \
                calculate_list_of_non_dominated_solutions(list_of_sorted_solutions)
            print_profit_and_weight_of_solutions_with_nd_information(
                list_of_sorted_solutions, list_of_non_dominated_solutions)
            # print_profit_and_weight_of_solutions(list_of_sorted_solutions)
            print("SOLUCOES NAO DOMINADAS:")
            print(calculate_list_of_non_dominated_solutions(list_of_sorted_solutions))


if __name__ == "__main__":
    main()
    sys.exit(0)
