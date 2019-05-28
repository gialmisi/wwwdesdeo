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
        "and desired number of generated points.", }

    def __init__(self):
        self.method = ENAUTILUS(RiverPollution(), SciPyDE)
        self.user_iters = None
        self.current_iter = None
        self.Ns = None

        self.state = Problem.states[0]

    def step(self):
        if self.state == Problem.states[0]:  # Initialization
            if not self.user_iters or not self.curses_iter or not self.Ns:
                return 1, Problem.responses[1]

        else:
            return 0, Problem.responses[0]

    def initialize(self, user_iters, Ns):
        pass
