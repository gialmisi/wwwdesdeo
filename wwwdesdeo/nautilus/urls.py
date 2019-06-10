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
    # path("0/", views.pollution_problem_initialize,
    #      name="pollution_problem_initialize"),
    # path("0/interactive/", views.pollution_problem_interactive,
    #      name="pollution_problem_interactive"),
    ]
