from sympy import latex

from expression_parser import (expressions_example,
                               symbols_example,
                               variables_example)


def analytical_problem_to_latex(expressions, symbols, variables):
    """Generates latex code for an analytical problem to be used with a template.

    :param expressions: List of sympy functions representing objectives
    :param symbols: A list of symbols presents in the functions
    :param variables: A list of dicts with bounds and initial values for each variable.
    :returns: A dict latex code
    :rtype: dict

    """

    counter = 1
    latex_objectives = []
    for expr in expressions:
        latex_objectives.append((
            latex("f_"+str(counter)+" = " + expr["expression"]),
            latex(expr["lower_bound"]),
            latex(expr["upper_bound"]),
            # expr["maximize"], TODO
        ))
        counter += 1

    latex_variables = []
    for (ind, sym) in enumerate(symbols):
        latex_variables.append((
            latex(sym),
            variables[ind][sym+"_upper_bound"],
            variables[ind][sym+"_lower_bound"],
            variables[ind][sym+"_initial_value"],
        ))

    return latex_objectives, latex_variables


# analytical_problem_to_latex(expressions_example,
#                             symbols_example,
#                             variables_example)
