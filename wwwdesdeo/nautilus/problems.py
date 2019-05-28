import os

from desdeo.method import ENAUTILUS
from desdeo.optimization import PointSearch, SciPyDE
from desdeo.problem import PreGeneratedProblem
from desdeo.problem.toy import RiverPollution

example_path = os.path.dirname(
    "/home/kilo/workspace/www-desdeo/wwwdesdeo/nautilus/")

def asdfsafsdf():
    method = ENAUTILUS(RiverPollution(), SciPyDE)


    method.user_iters = 5
    method.current_iter = 5
    method.Ns = 5
    print(method.next_iteration(preference=(None, None)))


class Problem():
    states = ["INITIALIZATION", "INTERACTIVE", "PROCESSING"]
    responses = {
        0: "Something went wrong...",
        1: "Please set the desired amount of iterations "
        "and desired number of generated points.",
        2: "Interactive", }

    def __init__(self):
        self.method = ENAUTILUS(RiverPollution(), SciPyDE)
        self.user_iters = None
        self.current_iter = None
        self.Ns = None
        self.nadir = self.method.problem.nadir
        self.ideal = self.method.problem.ideal

        self.state = Problem.states[0]

    def step(self, preference=(None, None)):
        if self.state == Problem.states[0]:  # Initialization
            if not self.user_iters or not self.curses_iter or not self.Ns:
                return 1, Problem.responses[1]

        elif self.state == Problem.states[1]:
            bounds_and_points = self.method.next_iteration(
                preference=preference)
            results = {
                "lower_bounds": [entry[0] for entry in bounds_and_points],
                "points": [entry[1] for entry in bounds_and_points],
                "nadir": self.nadir,
                "ideal": self.ideal,
                "total_iters": self.user_iters,
                "current_iter": self.current_iter,
                }
            return 2, Problem.responses[2], results

        else:
            return 0, Problem.responses[0]

    def initialize(self, user_iters, Ns):
        self.user_iters = user_iters
        self.current_iter = self.user_iters
        self.Ns = Ns
        
        #### APPLY THESE TO THE METHOD !!! ####

        self.state = Problem.states[1]
