from django.shortcuts import render
from django.http import HttpResponse

from .problems import Problem
from .models import pre_defined_problem_list
from .forms import InitializationForm, InteractiveForm

PROBLEM = None


def index(request):
    """Shows the user the available problems. At the moments, only
    pre-defined problems available."""
    context = {"available_problems_list": pre_defined_problem_list}
    return render(request, "nautilus/index.html", context)


def pollution_problem_initialize(request):
    global PROBLEM
    # PROBLEM is now initialized twice!
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
                               user_iters, generated_points), }

                PROBLEM.initialize(user_iters, generated_points)
                return render(request, "nautilus/interactive.html", context)

        else:
            form = InitializationForm()

            context["form"] = form
            return render(request, "nautilus/initialization.html", context)

    context = {"message": "Problem returned response 0"
               ", something has gone wrong..."}
    return render(request, "nautilus/error.html", context)


def pollution_problem_interactive(request):
    global PROBLEM
    code, description, results = PROBLEM.step()
    context = {"message": description, "results": results}

    if code == 2:  # Interactive mode
        print(results["points"])
        form = InteractiveForm(results["points"], request.POST)
        if form.is_valid():
            data = form.cleaned_data
            return render(request, "nautilus/interactive.html", context)

        else:
            form = InteractiveForm(results["points"])

            context["form"] = form
            print("hello")
            print(results["points"])
            print("hello")
            return render(request, "nautilus/interactive.html", context)

    return render(request, "nautilus/error.html", {"message": "What?"})
