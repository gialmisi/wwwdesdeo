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
    {'expression': 'x + y + z', 'lower_bound': -50.0, 'upper_bound': 50.0},
    {'expression': 'x - z / y * 3', 'lower_bound': -33.0, 'upper_bound': 40.0},
    {'expression': '10 * x + 9', 'lower_bound': -100, 'upper_bound': 600},
    ]
__example_variables = [
    {'x_lower_bound': 0, 'x_upper_bound': 10, 'x_initial_value': 5},
    {'y_lower_bound': -5, 'y_upper_bound': 5, 'y_initial_value': 0},
    {'z_lower_bound': 15, 'z_upper_bound': 20, 'z_initial_value': 17.5},
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

    return lamargs, expr.free_symbols, expr


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
    sympy_exprs = []  # the sympy expressions

    for expr in expression:
        fun, symbols, sympy_expr = exprs_to_lambda(expr["expression"])
        unique_symbols |= symbols  # unision
        results.append((
            fun,
            expr["lower_bound"],
            expr["upper_bound"],
            ))
        sympy_exprs.append(expr)

    unique_symbols_str = sorted(map(str, (unique_symbols)))

    return results, unique_symbols_str, sympy_exprs


_, symbols_example, expressions_example = parse(__example_valid)
variables_example = __example_variables

# print(parsed[0][0]({'t': -111, 'y': 2, 'z': 3, 'x': 1}))
