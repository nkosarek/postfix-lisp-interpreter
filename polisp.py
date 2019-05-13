import sys
from funcs import *

# TODO:
#   x Add variables
#   - Add functions
#       - Add lambda
#   - Add parsing of strings
#   - Add true/nil
#   - Validate more than just parentheses in parse()
#   - Add more built-in functions


class LispList(list):
    def __init__(self, l=None):
        super(LispList, self).__init__(l)


class Interpreter(object):
    def __init__(self, filename):
        self.scopes = [FunctionScope()]
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
            elif char == "'":
                exprs[len(exprs) - 1] = LispList(exprs[len(exprs) - 1])
            elif char.isspace() and atom != "":
                if atom.isdigit():
                    atom = int(atom)
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
            if atom.isdigit():
                atom = int(atom)
            exprs.append(atom)
        return exprs

    def eval(self):
        for expr in self.exprs:
            if not isinstance(expr, LispList):
                print self.eval_expr(expr)

    def eval_expr(self, expr):
        args = []
        for i in xrange(len(expr)):
            e = expr[i]
            if isinstance(e, LispList):
                args.append(e)
            elif isinstance(e, list):
                args.append(self.eval_expr(e))
            elif i == len(expr) - 1:
                curr_scope = self.scopes[0]
                return curr_scope.variables[e](curr_scope.variables, *args)
            else:
                args.append(e)
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
