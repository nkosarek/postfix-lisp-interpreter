import lisp_util as util
import uuid


class FunctionScope(object):
    def __init__(self, parent_vars=None):
        if parent_vars is None:
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
                "lambda": define_lambda,
                "if": if_condition,
                "defun": define_function,
                "print": print_value,
            }
        else:
            self.variables = dict(parent_vars)

    def add_variable(self, identifier, val):
        self.variables[identifier] = val


def add(scopes, *args):
    val0 = util.eval_var_if_possible(scopes, args[0])
    for val in args[1:]:
        val0 += util.eval_var_if_possible(scopes, val)
    return val0


def subtract(scopes, *args):
    val0 = util.eval_var_if_possible(scopes, args[0])
    for val in args[1:]:
        val0 -= util.eval_var_if_possible(scopes, val)
    return val0


def multiply(scopes, *args):
    result = 1
    for val in args:
        result *= util.eval_var_if_possible(scopes, val)
    return result


def divide(scopes, *args):
    val0 = util.eval_var_if_possible(scopes, args[0])
    for val in args[1:]:
        val0 /= util.eval_var_if_possible(scopes, val)
    return val0


def equals(scopes, *args):
    val0 = util.eval_var_if_possible(scopes, args[0])
    for val in args[1:]:
        if val0 != util.eval_var_if_possible(scopes, val):
            return False
    return True


def less_than(scopes, *args):
    val0 = util.eval_var_if_possible(scopes, args[0])
    for val in args[1:]:
        if val0 >= util.eval_var_if_possible(scopes, val):
            return False
    return True


def greater_than(scopes, *args):
    val0 = util.eval_var_if_possible(scopes, args[0])
    for val in args[1:]:
        if val0 <= util.eval_var_if_possible(scopes, val):
            return False
    return True


def less_than_or_equal(scopes, *args):
    val0 = util.eval_var_if_possible(scopes, args[0])
    for val in args[1:]:
        if val0 > util.eval_var_if_possible(scopes, val):
            return False
    return True


def greater_than_or_equal(scopes, *args):
    val0 = util.eval_var_if_possible(scopes, args[0])
    for val in args[1:]:
        if val0 < util.eval_var_if_possible(scopes, val):
            return False
    return True


def if_condition(scopes, *args):
    for i in xrange(len(args)):
        condition = args[i]
        # else case
        if i == len(args) - 1:
            return util.eval_expr(scopes, condition[0])
        # ifs
        elif util.eval_expr(scopes, condition[0]):
            return util.eval_expr(scopes, condition[1])


def define_variable(scopes, *args):
    assert len(args) == 2
    val = util.eval_var_if_possible(scopes, args[1])
    scopes[0].variables[args[0]] = val
    return val


def define_lambda(scopes, *args):
    assert len(args) == 2
    name = uuid.uuid4().hex
    params = args[0]
    body = list(args[1])

    return define_function_base(scopes, name, params, body)


def define_function(scopes, *args):
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = list(args[2])

    return define_function_base(scopes, name, params, body)


def define_function_base(scopes, name, params, body):
    def func(lam_scopes, *lam_args):
        assert len(params) == len(lam_args)
        scope = FunctionScope(lam_scopes[0].variables)
        for i in xrange(len(params)):
            val = util.eval_var_if_possible(scopes, lam_args[i])
            scope.add_variable(params[i], val)
        # for key in scope.variables:
        #     print "{:>10}".format(key), ":", scope.variables[key]
        lam_scopes.insert(0, scope)
        result = util.eval_exprs(lam_scopes, body)
        lam_scopes.pop(0)
        return result

    scopes[0].variables[name] = func
    return name


def print_value(scopes, *args):
    val = util.eval_var_if_possible(scopes, args[0])
    print val
