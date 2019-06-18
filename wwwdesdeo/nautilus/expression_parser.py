import re
import inspect

from sympy import sympify
from sympy.utilities.lambdify import lambdify

__example = [
    {'expression': 'x + y + z', 'lower_bound': 0.0, 'upper_bound': 5.0},
    {'expression': 'sin(z) + x**4 - 1/y', 'lower_bound': 33, 'upper_bound': 40.0},
    {'expression': 'FROM TABLE DROP *', 'lower_bound': -1, 'upper_bound': -1},
    ]

__example_valid = [
    {'expression': 'x + y + z', 'lower_bound': 0.0, 'upper_bound': 5.0},
    {'expression': 'x - z / y * 3', 'lower_bound': 33, 'upper_bound': 40.0},
    {'expression': '10 * x + 9', 'lower_bound': -1, 'upper_bound': 1},
    ]

# Match for basic artihmetic operators
__match_arithmetics = r'^(([0-9]|[a-z])+ ([\+,\-,\*,\/] ([0-9]|[a-z])*)+)*$'


class ExpressionException(Exception):
    pass


def exprs_to_lambda(str_expr):
    expr = sympify(str_expr)

    lam = lambdify(expr.free_symbols, expr)

    def lamargs(kwargs):
        args = inspect.getfullargspec(lam)[0]
        if (len(args) > len(kwargs)):
            raise ExpressionException("Too few arguments supplied!")

        stripped = {str(k): kwargs[k] for k in set(args)}
        return lam(**stripped)

    return lamargs, expr.free_symbols


def free_symbols_dict(str_expr):
    expr = sympify(str_expr)

    args = {str(k): None for k in expr.free_symbols}

    return args


def expressions_are_valid(expressions):
    for expr in expressions:
        if re.match(__match_arithmetics, expr["expression"]):
            print("Valid expression: ", expr["expression"])
        else:
            raise ExpressionException(
                "Invalid expression encountered: " + expr["expression"])

    return True


def parse(expression):
    if not expressions_are_valid(expression):
        return False

    results = []  # contains (function, low_b, up_b)
    unique_symbols = set()

    for expr in expression:
        fun, symbols = exprs_to_lambda(expr["expression"])
        unique_symbols |= symbols  # unision
        results.append((
            fun,
            expr["lower_bound"],
            expr["upper_bound"],
            ))

    unique_symbols_str = sorted(map(str, (unique_symbols)))

    return results, unique_symbols_str


# parsed, symbols = parse(__example_valid)

# print(parsed[0][0]({'t': -111, 'y': 2, 'z': 3, 'x': 1}))
