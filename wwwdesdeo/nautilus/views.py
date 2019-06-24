from django.shortcuts import render, redirect, reverse

import stateful_view as sf
import models as m
from .forms import (InitializationForm,
                    MethodInitializationForm,
                    IterationForm,
                    AnalyticalProblemInputFormSet,
                    VariableFormsFactory,)
from .expression_parser import parse, ExpressionException
from .misc import analytical_problem_to_latex


def index(request):
    """Handles the initial page where the user can define a problem to
    be solved and other relevant parameters related to the NAUTILIS-family
    of interactive methods.

    :param request: Contains GET and POST requests encoded in a dict
    :returns: A Http response with an html page
    :rtype: HttpResponse

    """
    context = {
        "available_methods": m.available_methods,
        "available_optimizers": m.available_optimizers,
        "problems": m.problems,
    }

    if request.method == "POST":
        form = InitializationForm(
            m.available_methods,
            m.available_optimizers,
            m.problems,
            request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if data["problem"] == "Custom":
                    # ask the DM to specify a custom problem
                    method = data["interactive_method"]
                    optimizer = data["optimizer"]

                    # Save the options for later use
                    sf.method = method
                    sf.optimizer = optimizer
                    return redirect(
                        reverse("analytical_problem_input_objectives"))
                else:
                    method = data["interactive_method"]
                    optimizer = data["optimizer"]
                    problem = data["problem"]

                    sf_view = sf.available_method_views_d[method](
                        method,
                        optimizer,
                        problem)
                    sf.current_view = sf_view
                    # Initialize the chosen method
                    return redirect(reverse("method_initialization"))
            except KeyError as e:
                context["message"] = "Key error " + str(e)
                template = "nautilus/error.html"

        else:
            context["message"] = "Form is invalid"
            template = "nautilus/error.html"

    else:
        # If request is GET, initialize the form
        form = InitializationForm(
            m.available_methods,
            m.available_optimizers,
            m.problems)
        context["form"] = form
        template = "nautilus/index.html"

    return render(request, template, context)


def method_initialization(request):
    """Handles the page where the user can specify method-specific
    parameters in the initialization phase of the method.

    :param request: Contains GET and POST requests encoded in a dict
    :returns: A Http response with an html page
    :rtype: HttpResponse

    """
    # Every method should have their own template
    template_dir = "nautilus/" + sf.current_view.template_dir
    template = template_dir + "/init.html"
    # Every method has its' own requirements for initialization
    requirements = sf.current_view.initialization_requirements

    context = {
        "requirements": requirements,
        "description": sf.current_view.help["description"],
        "title": sf.current_view.help["name"],
        }
    print(request)
    if request.method == "POST":
        form = MethodInitializationForm(
            requirements,
            request.POST)
        if form.is_valid():
            data = form.cleaned_data
            sf.current_view.initialize(**data)
            # Start iterating
            return redirect(reverse("method_iteration"))
        else:
            context["message"] = "Form is invalid"
            template = "nautilus/error.html"
    else:
        form = MethodInitializationForm(
            requirements)
        context["form"] = form
        return render(request, template, context)

    return render(request, template, context)


def method_iteration(request):
    """Generates pages with relevant information and interactive features
    to hande the iterative phase of a NAUTILUS method.

    :param request: Contains GET and POST requests encoded in a dict
    :returns: A Http response with an html page
    :rtype: HttpResponse

    """
    # Every method should have their own templates
    template_dir = "nautilus/" + sf.current_view.template_dir
    template = template_dir + "/iterate.html"
    # Every method has its' own preference requirements for iterating
    preferences = sf.current_view.preference_requirements
    context = {}
    context["title"] = "Iterating"

    # Iterate for the first time
    if sf.current_view.is_first_iteration:
        # iterate with no preferences
        sf.current_view.iterate()

    context["forms"] = {}
    last_results = sf.current_view.last_iteration
    context["results"] = last_results
    total_iterations = sf.current_view.user_iters
    current_iteration = sf.current_view.user_iters -\
        sf.current_view.current_iter
    context["current_iteration"] = current_iteration
    context["total_iterations"] = total_iterations

    if request.method == "POST":
        for pref in preferences:
            form = IterationForm(
                range(len(last_results[pref])),
                request.POST)
            context["forms"][pref] = form

        for form in context["forms"].values():
            if form.is_valid():
                data = form.cleaned_data
                index = int(data["choice"])
                # convert to a tuple containing lists of floats
                preference = list(zip(*last_results.values()))[index]
                # check end condition
                if current_iteration + 1 == total_iterations:
                    sf.current_view.iterate(preference)
                    return redirect(reverse("method_results"))

                sf.current_view.iterate(preference)
                return redirect(reverse("method_iteration"))
            else:
                context["message"] = "Form is invalid"
                return redirect(reverse("index"))
    else:
        for pref in preferences:
            form = IterationForm(
                range(len(last_results[pref])))
            context["forms"][pref] = form

        return render(request, template, context)

    return redirect(reverse("index"))


def method_results(request):
    """ Generates a page to shows the final results.

    :param request: Contains GET and POST requests encoded in a dict
    :returns: A Http response with an html page
    :rtype: HttpResponse

    """
    # Every method should have their own templates
    template_dir = "nautilus/" + sf.current_view.template_dir
    template = template_dir + "/iterate.html"
    final_results = sf.current_view.last_iteration
    context = {}
    context["title"] = "Results"
    context["results"] = final_results

    return render(request, template, context)


def analytical_problem_input_objectives(request):
    """Generates a page for the user to input objective functions and their limits.
    TODO: Ask the user whether the objective is to be maximixed or minimized.

    :param request: Contains GET and POST requests encoded in a dict
    :returns: A Http response with an html page
    :rtype: HttpResponse

    """
    template = "nautilus/analytical_problem_input_objectives.html"
    context = {}
    context["title"] = "Objective specification"

    if request.method == "POST":
        # handle filled form
        formset = AnalyticalProblemInputFormSet(request.POST)
        if formset.is_valid():
            data = formset.cleaned_data
            try:
                expressions, symbols, sympy_exprs = parse(data)
                sf.current_sympy_exprs = sympy_exprs
                sf.current_expressions = expressions
                sf.current_symbols = symbols
                return redirect(reverse("analytical_problem_input_variables"))

            except ExpressionException as err:
                context["message"] = str(err)
                template = "nautilus/error.html"
                return render(request, template, context)

        else:
            context["message"] = "Form is invalid"
            template = "nautilus/error.html"
            return render(request, template, context)
    else:
        formset = AnalyticalProblemInputFormSet()
        context["formset"] = formset

    return render(request, template, context)


def analytical_problem_input_variables(request):
    """Based on the objectives (stored in stateful_view), generates a page where
    the user can specify limits for the variables present in the objectives.

    :param request: Contains GET and POST requests encoded in a dict
    :returns: A Http response with an html page
    :rtype: HttpResponse

    """
    template = "nautilus/analytical_problem_input_variables.html"
    context = {}
    context["title"] = "Decision variable specification"

    if request.method == "POST":
        # handle filled form
        sf.current_variables = []
        forms = VariableFormsFactory(sf.current_symbols, request.POST)
        for f in forms:
            if f.is_valid():
                sf.current_variables.append(f.cleaned_data)
            else:
                template = "nautilus/error.html"
                context["message"] = "Form is invalid"
                return render(request, template, context)

        return redirect(reverse("analytical_problem_confirm"))
    else:
        # create empty form
        forms = VariableFormsFactory(sf.current_symbols)
        context["forms"] = forms

    return render(request, template, context)


def analytical_problem_confirm(request):
    """Shows the problem's objectives and limits, variables and limits, and renders
    them in LaTex.

    :param request: Contains GET and POST requests encoded in a dict
    :returns: A Http response with an html page
    :rtype: HttpResponse

    """
    template = "nautilus/analytical_problem_confirm.html"
    context = {}
    context["title"] = "Confirm analytical problem"
    l_objs, l_vars = analytical_problem_to_latex(
        sf.current_sympy_exprs,
        sf.current_symbols,
        sf.current_variables)
    context["latex_objectives"] = l_objs
    context["latex_variables"] = l_vars

    return render(request, template, context)


def analytical_problem_optimize(request):
    """Performs all the necessary calls for the underlying stateful_view to be
    properly set up with the problem specicied by the user. Redirects to
    'method_initialization' when done.

    :param request: Contains GET and POST requests encoded in a dict
    :returns: A Http response with an html page
    :rtype: HttpResponse

    """
    # Create the analytical problem
    problem = sf.AnalyticalProblem(
        sf.current_expressions,
        sf.current_symbols,
        sf.current_variables
        )
    # Setup the stateful view
    sf_view = sf.available_method_views_d[sf.method](
        sf.method,
        sf.optimizer,
        problem)
    sf.current_view = sf_view
    return redirect(reverse("method_initialization"))
