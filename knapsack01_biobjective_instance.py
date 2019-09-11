# -*- coding: utf-8 -*-
from typing import Tuple


class Knapsack01BiobjectiveInstance:
    def __init__(self, name: str, n: int = 0, c: int = 0, z: int = 0) -> None:
        self.name = name
        self.n = n
        self.c = c
        self.z = z
        self.weight = []
        self.profit = []
        self.x_vector = []

    def add_item(self, profit: int, weight: int, x_value: int = -1):
        self.profit.append(profit)
        self.weight.append(weight)
        if x_value != -1:
            self.x_vector.append(x_value)

    def __str__(self) -> str:
        str_return = 'Nome Instancia: "%s"' % self.name
        str_return += '\nN: %d' % self.n
        str_return += '\nC: %d' % self.c
        if self.x_vector:
            for item_iter in range(self.n):
                str_return += \
                    '\n\t%d %d %d %d' % \
                    (item_iter, self.profit[item_iter],
                     self.weight[item_iter], self.x_vector[item_iter])
        else:
            for item_iter in range(self.n):
                str_return += \
                    '\n\t%d %d %d' % \
                    ((item_iter + 1), self.profit[item_iter], self.weight[item_iter])
        str_return += '\nZ: %d' % self.z
        return str_return


class Knapsack01BiobjectiveSolution:
    def __init__(self, kp_instance: Knapsack01BiobjectiveInstance) -> None:
        self.kp_instance = kp_instance
        self.x_vector = [0] * kp_instance.n
        self.__function_weight = self.__calculate_weight_solution
        self.__function_profit = self.__calculate_profit_solution
        self.__weight = 0
        self.__profit = 0

    def __calculate_profit_solution(self) -> int:
        # print("Calculando lucro da solucao...")
        self.__profit = sum([self.kp_instance.profit[i] for i, item in enumerate(self.x_vector) if item == 1])
        self.profit = self.__get_profit_solution
        return self.__profit

    def __calculate_weight_solution(self) -> int:
        # print("Calculando peso da solucao...")
        self.__weight = sum([self.kp_instance.weight[i] for i, item in enumerate(self.x_vector) if item == 1])
        self.weight = self.__get_weight_solution
        return self.__weight

    def profit(self) -> int:
        return self.__function_profit()

    def weight(self) -> int:
        return self.__function_weight()

    def __get_profit_solution(self) -> int:
        return self.__profit

    def __get_weight_solution(self) -> int:
        return self.__weight

    def update_weight_and_profit(self) -> None:
        self.__calculate_weight_solution()
        self.__calculate_profit_solution()

    def update_x_vector(self, position: int, new_value: int) -> Tuple[int, int]:
        old_value = self.x_vector[position]
        self.x_vector[position] = new_value
        if new_value != old_value:
            if new_value == 1:
                self.__weight += self.kp_instance.weight[position]
                self.__profit += self.kp_instance.profit[position]
            else:
                self.__weight -= self.kp_instance.weight[position]
                self.__profit -= self.kp_instance.profit[position]
        return self.__weight, self.__profit

    def is_valid(self) -> bool:
        return self.weight() <= self.kp_instance.c

    def __str__(self) -> str:
        str_return = 'Nome Instancia: "%s"' % self.kp_instance.name
        str_return += '\nN: %d' % self.kp_instance.n
        str_return += '\nC: %d' % self.kp_instance.c
        str_return += '\nSOLUCAO:'
        for i, item_binary_value in enumerate(self.x_vector):
            if item_binary_value == 1:
                str_return += \
                    '\n\t%d %d %d' % \
                    (i + 1, self.kp_instance.profit[i],
                     self.kp_instance.weight[i])
        str_return += '\nLUCRO TOTAL: %d' % self.profit()
        str_return += '\nPESO TOTAL: %d' % self.weight()
        return str_return
