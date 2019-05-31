from abc import abstractmethod, abstractproperty
import models as m

current_view = None


class NautilusView():
    def __init__(self,
                 method="ENAUTILUS",
                 optimizer="SciPyDE",
                 problem="River Pollution"
                 ):
        _method = m.available_methods_d[method]
        _optimizer = m.available_optimizers_d[optimizer]
        _problem = m.problems_d[problem]

        self._method = _method(_problem, _optimizer)
        self._nadir = self.method.problem.nadir
        self._ideal = self.method.problem.ideal
        self._initialized = False

    @property
    def method(self):
        return self._method

    @property
    def nadir(self):
        return self._nadir

    @property
    def ideal(self):
        return self._ideal

    @property
    def initialized(self):
        return self._initialized

    @initialized.setter
    def initialized(self, val):
        self._initialized = val

    @abstractmethod
    def get_initialization_requirements(self):
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def iterate(self):
        pass

    @abstractmethod
    def template_dir(self):
        pass


class ENautilusView(NautilusView):
    def __init__(self,
                 method="ENAUTILUS",
                 optimizer="SciPyDE",
                 problem="River Pollution"
                 ):

        super().__init__(method, optimizer, problem)
        self.__template_dir = "ENAUTILUS"
        self.__user_iters = 5
        self.__current_iter = self.user_iters
        self.__n_generated_points = 10

    @property
    def template_dir(self):
        return self.__template_dir

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

    def get_initialization_requirements(self):
        reqs = [
            "User iterations",
            "Number of generated points",
            ]
        return reqs

    @property
    def initialized(self):
        return self._initialized

    @initialized.setter
    def initialized(self, val):
        self._initialized = val

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


available_method_views_d = {
    "ENAUTILUS": ENautilusView,
    }
