# -*- coding: utf-8 -*-
from enum import IntEnum, Enum


class Const(IntEnum):
    INSTANCE_FILE = 1
    OUTPUT_FILE = 2
    INSTANCE_NUMBER_INSIDE_FILE = 3
    EXECUTION_TIME = 4


class StrConst(Enum):
    LINE_COMMAND_PARAM_INSTANCE_NUMBER_INSIDE_FILE = "-i"
    LINE_COMMAND_PARAM_EXECUTION_TIME = "-t"
