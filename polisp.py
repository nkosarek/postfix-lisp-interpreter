import sys
from funcs import *

# TODO:
#   - Add parsing of strings
#   - Add more built-in functions
#   - Add variables
#   - Add true/nil
#   - Validate more than just parentheses in parse()
#   - Add functions


class Interpreter(object):
    def __init__(self, filename):
        with open(filename, "r") as fp:
            self.exprs = self.parse(fp, terminator="")
            print self.exprs

    @staticmethod
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
        while char != terminator:
            # Reached EOF, but not supposed to yet
            if char == "":
                raise Exception("Missing terminating '%s'" % terminator)
            # Found an invalid extra ')'
            elif char == ")":
                raise Exception("Extra ')' found at file location " + str(fp.tell()))
            # Completed an atom with a space
            elif char.isspace() and atom != "":
                exprs.append(atom)
                atom = ""
            # Start nested list
            elif char == "(":
                exprs.append(Interpreter.parse(fp))
            # Add to current atom
            elif not char.isspace():
                atom += char
            # Get next char
            char = fp.read(1)
        # Last atom is adjacent to terminator
        if atom != "":
            exprs.append(atom)
        return exprs

    def eval(self):
        for expr in self.exprs:
            print Interpreter.eval_expr(expr)

    @staticmethod
    def eval_expr(expr):
        args = []
        for e in expr:
            if isinstance(e, list):
                args.append(Interpreter.eval_expr(e))
            elif e in BuiltInFuncs:
                return BuiltInFuncs[e](*args)
            elif e.isdigit():
                args.append(int(e))
            else:
                raise Exception("Unsupported atom: " + e)
        return args


if __name__ == "__main__":
    print "**** PoLisp Interpreter ****"
    argc = len(sys.argv)
    if argc == 1:
        print "FAILURE: stdin not yet supported."
        print "\tUsage: ./%s <filename>" % __file__.split("/")[-1]
        exit(1)
        # interp = Interpreter()
    else:
        interp = Interpreter(filename=sys.argv[1])
        if argc > 2:
            print "Expected only one argument. Ignoring the rest:", sys.argv[2:]

    interp.eval()
