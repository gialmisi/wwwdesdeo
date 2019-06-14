from django.shortcuts import render, redirect, reverse

import stateful_view as sf
import models as m
from .forms import (InitializationForm,
                    MethodInitializationForm,
                    IterationForm,
                    AnalyticalProblemInputFormSet)


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
            if data["problem"] == "Custom":
                # ask the DM to specify a custom problem
                return redirect(reverse("analytical_problem_input"))
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
        "help": sf.current_view.help,
        }

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
                print(current_iteration)
                print(total_iterations)
                if current_iteration + 1 == total_iterations:
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
    # Every method should have their own templates
    template_dir = "nautilus/" + sf.current_view.template_dir
    template = template_dir + "/iterate.html"
    final_results = sf.current_view.last_iteration
    context = {}
    context["results"] = final_results

    return render(request, template, context)


def analytical_problem_input(request):
    template = "nautilus/analytical_problem_input.html"
    context = {}

    if request.method == "POST":
        # handle filled form
        pass
    else:
        formset = AnalyticalProblemInputFormSet()
        context["formset"] = formset
        context["heading"] = "heading"

    return render(request, template, context)
