from django.shortcuts import render
from django.http import HttpResponse

from .problems import Problem
from .models import pre_defined_problem_list
from .forms import InitializationForm

PROBLEM = None


def index(request):
    """Shows the user the available problems. At the moments, only
    pre-defined problems available."""
    context = {"available_problems_list": pre_defined_problem_list}
    return render(request, "nautilus/index.html", context)


def pollution_problem_initialize(request):
    global PROBLEM
    PROBLEM = Problem()
    code, description = PROBLEM.step()

    if code == 1:  # Initialization
        context = {"message": description}
        if request.method == "POST":
            form = InitializationForm(request.POST)

            if form.is_valid():
                data = form.cleaned_data
                user_iters = data["user_iters"]
                generated_points = data["generated_points"]
                PROBLEM.initialize(user_iters, generated_points)

                context = {"message": "Problem initialized successfully with "
                           "{0} total iters and {1} points to be generated "
                           "for each iteration.".format(
                               user_iters, generated_points),}

                return render(request, "nautilus/interactive.html", context)

        else:
            form = InitializationForm()

            context["form"] = form
            return render(request, "nautilus/initialization.html", context)

    context = {"message": "Problem returned response 0"
               ", something has gone wrong..."}
    return render(request, "nautilus/error.html", context)
