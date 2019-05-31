from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("0/", views.pollution_problem_initialize,
    #      name="pollution_problem_initialize"),
    # path("0/interactive/", views.pollution_problem_interactive,
    #      name="pollution_problem_interactive"),
    ]
