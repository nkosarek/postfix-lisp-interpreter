import sys
from func_defs import *

# TODO:
#   x Add variables
#   x Add functions
#       x Add lambda
#   x Add if/else
#   x Test recursive case
#   - Add parsing of strings
#   - Add true/nil
#   - Validate more than just parentheses in parse()
#   - Add more built-in functions


class Interpreter(object):
    def __init__(self, filename):
        self.scopes = [FunctionScope()]
        with open(filename, "r") as fp:
            self.exprs = util.parse(fp, terminator="")

    def eval(self):
        for expr in self.exprs:
            print "*", expr
            if not isinstance(expr, util.LispList):
                print "=>", util.eval_expr(self.scopes, expr)
            else:
                print "=>", expr


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
