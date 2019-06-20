from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("init.html", views.method_initialization,
         name="method_initialization"),
    path("iteration.html", views.method_iteration,
         name="method_iteration"),
    path("results.html", views.method_results,
         name="method_results"),
    path("analytical_problem_input_objectives.html",
         views.analytical_problem_input_objectives,
         name="analytical_problem_input_objectives"),
    path("analytical_problem_input_variables.html",
         views.analytical_problem_input_variables,
         name="analytical_problem_input_variables"),
    path("analytical_problem_confirm.html",
         views.analytical_problem_confirm,
         name="analytical_problem_confirm"),
    path("analytical_problem_optimize.html",
         views.analytical_problem_optimize,
         name="analytical_problem_optimize"),
    ]
