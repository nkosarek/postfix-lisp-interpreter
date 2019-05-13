def is_not_primitive(value):
    return not isinstance(value, (bool, int, long, list))


def add(variables, *args):
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        val0 += val
    return val0


def subtract(variables, *args):
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        val0 -= val
    return val0


def multiply(variables, *args):
    result = 1
    for val in args:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        result *= val
    return result


def divide(variables, *args):
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        val0 /= val
    return val0


def equals(variables, *args):
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 != val:
            return False
    return True


def less_than(variables, *args):
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 >= val:
            return False
    return True


def greater_than(variables, *args):
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 <= val:
            return False
    return True


def less_than_or_equal(variables, *args):
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 > val:
            return False
    return True


def greater_than_or_equal(variables, *args):
    val0 = args[0]
    if is_not_primitive(val0) and val0 in variables:
        val0 = variables[val0]
    for val in args[1:]:
        if is_not_primitive(val) and val in variables:
            val = variables[val]
        if val0 < val:
            return False
    return True


def define_variable(variables, *args):
    assert len(args) == 2
    variables[args[0]] = args[1]
    return args[1]
