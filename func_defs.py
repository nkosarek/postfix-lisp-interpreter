import lisp_util
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
            }
        else:
            self.variables = dict(parent_vars)

    def add_variable(self, identifier, val):
        self.variables[identifier] = val


def is_not_primitive(value):
    return not isinstance(value, (bool, int, long, list))


def add(scopes, *args):
    variables = scopes[0].variables
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        val0 += val
    return val0


def subtract(scopes, *args):
    variables = scopes[0].variables
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        val0 -= val
    return val0


def multiply(scopes, *args):
    variables = scopes[0].variables
    result = 1
    for val in args:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        result *= val
    return result


def divide(scopes, *args):
    variables = scopes[0].variables
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        val0 /= val
    return val0


def equals(scopes, *args):
    variables = scopes[0].variables
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 != val:
            return False
    return True


def less_than(scopes, *args):
    variables = scopes[0].variables
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 >= val:
            return False
    return True


def greater_than(scopes, *args):
    variables = scopes[0].variables
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 <= val:
            return False
    return True


def less_than_or_equal(scopes, *args):
    variables = scopes[0].variables
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 > val:
            return False
    return True


def greater_than_or_equal(scopes, *args):
    variables = scopes[0].variables
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 < val:
            return False
    return True


def if_condition(scopes, *args):
    for i in xrange(len(args)):
        condition = args[i]
        # else case
        if i == len(args) - 1:
            return condition[0]
        # ifs
        elif lisp_util.eval_expr(scopes, condition[0]):
            return condition[1]


def define_variable(scopes, *args):
    assert len(args) == 2
    variables = scopes[0].variables
    val = args[1]
    if is_not_primitive(val) and val in variables:
        val = variables[val]
    variables[args[0]] = val
    return val


def define_lambda(scopes, *args):
    assert len(args) == 2
    params = args[0]
    body = list(args[1])

    def func(lam_scopes, *lam_args):
        assert len(params) == len(lam_args)
        scope = FunctionScope(lam_scopes[0].variables)
        for i in xrange(len(params)):
            val = lam_args[i]
            if is_not_primitive(val) and val in scope.variables:
                val = scope.variables[val]
            scope.add_variable(params[i], val)
        lam_scopes.insert(0, scope)
        result = lisp_util.eval_exprs(lam_scopes, body)
        lam_scopes.pop(0)
        return result

    identifier = uuid.uuid4().hex
    scopes[0].variables[identifier] = func
    return identifier


def define_function(scopes, *args):
    pass
