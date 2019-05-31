from django.shortcuts import render

import stateful_view as sf
import models as m
from .forms import InitializationForm


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
                # ask the DM to specify the problems
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
                sf.sf_view = sf_view
                return method_initialization(request)
        else:
            context["message"] = "Request not of type POST"
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
    template_dir = "nautilus/" + sf.sf_view.template_dir
    requirements = sf.sf_view.get_initialization_requirements()
    print(requirements)
    context = {
        "requirements": requirements,
        }
    # TODO create form to hand the requirements
    return render(request,
                  template_dir + "/init.html",
                  context)

    #     if code == 1:  # Initialization
    #     context = {"message": description}
    #     if request.method == "POST":
    #         form = InitializationForm(request.POST)

    #         if form.is_valid():
    #             data = form.cleaned_data
    #             user_iters = data["user_iters"]
    #             generated_points = data["generated_points"]
    #             PROBLEM.initialize(user_iters, generated_points)

    #             context = {"message": "Problem initialized successfully with "
    #                        "{0} total iters and {1} points to be generated "
    #                        "for each iteration.".format(
    #                            user_iters, generated_points), }

    #             PROBLEM.initialize(user_iters, generated_points)
    #             return render(request, "nautilus/interactive.html", context)

    #     else:
    #         form = InitializationForm()

    #         context["form"] = form
    #         return render(request, "nautilus/initialization.html", context)
    # return render(request, "nautilus/index.html", context)


# def pollution_problem_initialize(request):
#     global PROBLEM
#     # PROBLEM is now initialized twice!
#     PROBLEM = Problem()
#     code, description = PROBLEM.step()

#     if code == 1:  # Initialization
#         context = {"message": description}
#         if request.method == "POST":
#             form = InitializationForm(request.POST)

#             if form.is_valid():
#                 data = form.cleaned_data
#                 user_iters = data["user_iters"]
#                 generated_points = data["generated_points"]
#                 PROBLEM.initialize(user_iters, generated_points)

#                 context = {"message": "Problem initialized successfully with "
#                            "{0} total iters and {1} points to be generated "
#                            "for each iteration.".format(
#                                user_iters, generated_points), }

#                 PROBLEM.initialize(user_iters, generated_points)
#                 return render(request, "nautilus/interactive.html", context)

#         else:
#             form = InitializationForm()

#             context["form"] = form
#             return render(request, "nautilus/initialization.html", context)

#     context = {"message": "Problem returned response 0"
#                ", something has gone wrong..."}
#     return render(request, "nautilus/error.html", context)


# def pollution_problem_interactive(request):
#     code, description, results = step_problem()
#     context = {"message": description, "results": results}

#     if code == 2:  # Interactive mode
#         print(results["points"])
#         form = InteractiveForm(request.POST)

#         if form.is_valid():
#             selection = form.cleaned_data["preferred_point"]
#             print(selection)
#             if selection < len(results["points"]):
#                 zh  = results["points"][selection-1]

#             return render(request, "nautilus/interactive.html", context)

#         else:
#             form = InteractiveForm()

#             context["form"] = form
#             return render(request, "nautilus/interactive.html", context)

#     return render(request, "nautilus/error.html", {"message": "What?"})


# def step_problem(preference=(None, None)):
#     global PROBLEM
#     code, description, results = PROBLEM.step(preference)
#     return code, description, results
