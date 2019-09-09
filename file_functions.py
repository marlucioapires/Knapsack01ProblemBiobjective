# -*- coding: utf-8 -*-
import csv
from knapsack01_biobjective_instance import Knapsack01BiobjectiveInstance


def read_next_line(csv_reader):
    try:
        row = next(csv_reader)
    except StopIteration:
        return None
    return row


def processate_instance_file(
        name_instance_file: str, instance_number: int = 1) -> Knapsack01BiobjectiveInstance:
    with open(name_instance_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        kp01_instance = None
        instance_count = 0
        previous_row = ""
        row = read_next_line(csv_reader)
        while row is not None:
            if row and row[0].split()[0].lower() == "n":
                instance_count += 1
                if instance_count == instance_number:
                    try:
                        n_value = int(row[0].split()[1])
                        row = read_next_line(csv_reader)
                        c_value = int(row[0].split()[1])
                        row = read_next_line(csv_reader)
                        z_value = int(row[0].split()[1])
                        read_next_line(csv_reader)
                        kp01_instance = \
                            Knapsack01BiobjectiveInstance(previous_row[0], n_value, c_value, z_value)
                        for i in range(n_value):
                            row = read_next_line(csv_reader)
                            kp01_instance.add_item(int(row[1]), int(row[2]), int(row[3]))
                        break
                    except (IndexError, TypeError, ValueError):
                        kp01_instance = None
                        break
            previous_row = row
            row = read_next_line(csv_reader)
    return kp01_instance
