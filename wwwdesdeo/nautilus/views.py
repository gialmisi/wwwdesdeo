from django.shortcuts import render, redirect, reverse

import stateful_view as sf
import models as m
from .forms import InitializationForm, MethodInitializationForm, IterationForm


def index(request):
    """Shows available methods and problems"""
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
                # TODO
                context["message"] = "Not implemented"
                template = "nautilus/error.html"
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
        form = InitializationForm(
            m.available_methods,
            m.available_optimizers,
            m.problems)
        context["form"] = form
        template = "nautilus/index.html"

    return render(request, template, context)


def method_initialization(request):
    # Every method should have their own template
    template_dir = "nautilus/" + sf.current_view.template_dir
    template = template_dir + "/init.html"
    # Every method has its' own requirements for initialization
    requirements = sf.current_view.initialization_requirements

    context = {
        "requirements": requirements,
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
    # Every method should have their own template
    template_dir = "nautilus/" + sf.current_view.template_dir
    template = template_dir + "/iterate.html"
    # Every method has its' own preference requirements for iterating
    preferences = sf.current_view.preference_requirements
    context = {}

    # Iterate for the first time
    if sf.current_view.first_iteration:
        # iterate with no preferences
        results = sf.current_view.iterate()
        context["results"] = results

    context["forms"] = {}
    if request.method == "POST":
        for pref in preferences:
            form = IterationForm(
                results[pref],
                request.POST)
            context["forms"][pref] = form

        for form in context["forms"]:
            if form.is_valid():
                # handle valid values
                pass
            else:
                # raise error
                pass
    else:
        for pref in preferences:
            form = IterationForm(
                results[pref])
            context["forms"][pref] = form
            print(context["forms"])

        return render(request, template, context)

    return redirect(reverse("index"))
