from desdeo.method import ENAUTILUS
from desdeo.optimization import SciPyDE
from desdeo.problem.toy import RiverPollution


class ENautilusView():
    def __init__(self, problem=RiverPollution(), method=SciPyDE):
        self.__method = ENAUTILUS(problem, method)
        self.__user_iters = 5
        self.__current_iter = self.user_iters
        self.__n_generated_points = 10
        self.__nadir = self.method.problem.nadir
        self.__ideal = self.method.problem.ideal
        self.__initialized = False

    @property
    def method(self):
        return self.__method

    @property
    def user_iters(self):
        return self.__user_iters

    @user_iters.setter
    def user_iters(self, val):
        self.__validate_is_positive(val)
        self.__user_iters = val

    @property
    def current_iter(self):
        return self.__current_iter

    @current_iter.setter
    def current_iter(self, val):
        self.__validate_is_positive(val)
        self.__current_iter = val

    @property
    def n_generated_points(self):
        return self.__n_generated_points

    @n_generated_points.setter
    def n_generated_points(self, val):
        self.__validate_is_positive(val)
        self.__n_generated_points = val

    @property
    def nadir(self):
        return self.__nadir

    @property
    def ideal(self):
        return self.__ideal

    @property
    def initialized(self):
        return self.__initialized

    @initialized.setter
    def initialized(self, val):
        self.__initialized = val

    def __validate_is_positive(self, val):
        if val < 1:
            raise ValueError("Value must be positive!")

    def initialize(self, user_iters, n_generated_points):
        self.user_iters = user_iters
        self.current_iter = self.user_iters
        self.n_generated_points = n_generated_points

        self.method.user_iters = self.user_iters
        self.method.current_iter = self.user_iters
        self.method.Ns = self.n_generated_points

        self.initialized = True

    def iterate(self, preference=(None, None)):
        results = self.method.next_iteration(
            preference=preference)

        results_d = {
            "lower_bounds": [entry[0] for entry in results],
            "points": [entry[1] for entry in results],
            }

        self.current_iter = self.method.current_iter

        return results_d
