def add(*args):
    return sum(args)


def subtract(*args):
    val0 = args[0]
    for val in args[1:]:
        val0 -= val
    return val0


def multiply(*args):
    prod = 1
    for val in args:
        prod *= val
    return prod


def divide(*args):
    quot = args[0]
    for val in args[1:]:
        quot /= val
    return quot


def equals(*args):
    val0 = args[0]
    for val in args[1:]:
        if val0 != val:
            return False
    return True


def less_than(*args):
    val0 = args[0]
    for val in args[1:]:
        if val0 >= val:
            return False
    return True


def greater_than(*args):
    val0 = args[0]
    for val in args[1:]:
        if val0 <= val:
            return False
    return True


def less_than_or_equal(*args):
    val0 = args[0]
    for val in args[1:]:
        if val0 > val:
            return False
    return True


def greater_than_or_equal(*args):
    val0 = args[0]
    for val in args[1:]:
        if val0 < val:
            return False
    return True
