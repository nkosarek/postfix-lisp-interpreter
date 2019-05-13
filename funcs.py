from func_defs import *


class FunctionScope(object):
    def __init__(self):
        self.variables = {
            "+": add,
            "-": subtract,
            "*": multiply,
            "/": divide,
            "=": equals,
            "<": less_than,
            ">": greater_than,
            "<=": less_than_or_equal,
            ">=": greater_than_or_equal,
            "def": define_variable,
        }
