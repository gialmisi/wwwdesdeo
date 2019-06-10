from sympy import sympify
from sympy.utilities.lambdify import lambdify


def exprs_to_lambda(str_expr):
    expr = sympify(str_expr)

    # args = {str(k): 0 for (k, _) in zip(expr.free_symbols,
    # expr.free_symbols)}

    lam = lambdify(expr.free_symbols, expr)
    return lam


def free_symbols_dict(str_expr):
    expr = sympify(str_expr)

    args = {str(k): None for k in expr.free_symbols}

    return args
