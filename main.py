# -*- coding: utf-8 -*-
from algorithms import solve_knapsack01_problem
from constants import Const, StrConst
from file_functions import processate_instance_file
from knapsack01_biobjective_instance import Knapsack01BiobjectiveSolution
import sys
from typing import Dict, List
from algorithms import *
import random


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
            solution = generate_ramdomic_solution_for_knapsack_01_problem(kp_instance)
            print("\nSOLUCAO GERADA ALEATORIAMENTE:")
            print(str(solution))
            print("SOLUCAO EH VALIDA? R: " + str(solution.is_valid()))
            print("APLICANDO MOVIMENTO NA SOLUCAO...")
            apply_movement_put_or_remove_item_in_randomic_position(solution)
            print("\nSOLUCAO APOS ALTERACAO:")
            print(str(solution))
            print("SOLUCAO EH VALIDA? R: " + str(solution.is_valid()))
            # print("LUCRO DA SOLUCAO: %d" % solution.profit())
            # print("PESO DA SOLUCAO: %d" % solution.weight())


if __name__ == "__main__":
    main()
    sys.exit(0)
