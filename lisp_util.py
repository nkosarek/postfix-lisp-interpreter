class LispList(list):
    def __init__(self, l=[]):
        super(LispList, self).__init__(l)


class LispString(str):
    def __init__(self, s=""):
        super(LispString, self).__init__(s)


def is_not_primitive(value):
    return not isinstance(value, (bool, int, long, list, LispString))


def eval_var_if_possible(scopes, var):
    if is_not_primitive(var) and var in scopes[0].variables:
        return scopes[0].variables[var]
    return var


def parse(fp, terminator=')'):
    """
    Parses a lisp file into a list of expressions.
    :param fp: File pointer to be parsed.
    :param terminator: Either ')' or "".
    :return: List of expressions.
    """
    exprs = []
    char = fp.read(1)
    atom = ""
    in_string = False
    while (char != terminator and not in_string) or in_string:
        # Reached EOF, but not supposed to yet
        if char == "" and in_string:
            raise Exception("Missing terminating \"")
        # Reached EOF, but not supposed to yet
        elif char == "":
            raise Exception("Missing terminating '%s'" % terminator)
        # Complete current string atom
        elif char == '"' and in_string:
            in_string = False
            exprs.append(atom)
            atom = ""
        # Add to current string atom
        elif in_string:
            atom += char
        # Found an invalid extra ')'
        elif char == ")":
            raise Exception("Extra ')' found at file location " + str(fp.tell()))
        # Start a string atom
        elif char == '"' and not in_string:
            in_string = True
            if atom != "":
                exprs.append(atom)
            atom = ""
        # Last atom was a plain list, not expression
        elif char == "'":
            exprs[len(exprs) - 1] = LispList(exprs[len(exprs) - 1])
        # Completed an atom with a space
        elif char.isspace() and atom != "":
            if atom.isdigit():
                atom = int(atom)
            exprs.append(atom)
            atom = ""
        # Start nested list
        elif char == "(":
            exprs.append(parse(fp))
        # Add to current atom
        elif not char.isspace():
            atom += char
        # Get next char
        char = fp.read(1)
    # Last atom is adjacent to terminator
    if atom != "":
        if atom.isdigit():
            atom = int(atom)
        exprs.append(atom)
    return exprs


def eval_exprs(scopes, exprs):
    """
    Evaluate a list of postfix lisp expressions recursively
    :param scopes: Function scope stack
    :param exprs: Expressions to evaluate
    :return: Result of last expression's evaluation
    """
    for expr in exprs:
        if not isinstance(expr, LispList):
            # print "*", expr
            result = eval_expr(scopes, expr)
            # print "=>", result
    return result


def eval_expr(scopes, expr):
    """
    Evaluate a postfix lisp expression recursively
    :param scopes: Function scope stack
    :param expr: Expressions to evaluate
    :return: Result of evaluation
    """
    if not isinstance(expr, list):
        return eval_var_if_possible(scopes, expr)

    args = []
    for i in xrange(len(expr)):
        e = expr[i]

        if not isinstance(e, LispList) and isinstance(e, list):
            e = eval_expr(scopes, e)

        if i == len(expr) - 1:
            curr_scope = scopes[0]
            # print e, "(", args, ")"
            return curr_scope.variables[e](scopes, *args)
        else:
            args.append(e)

    return args
