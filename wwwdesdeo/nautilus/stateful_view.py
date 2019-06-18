import models as m
from desdeo.problem import MOProblem
from expression_parser import parse


current_view = None


class AnalyticalProblem(MOProblem):
    def __init__(self, expressions, symbols):
        __nobj = len(expressions)
        # TODO: Handle no bounds
        # TODO: objective funcions names
        # TODO: maximize of minimize?
        self.__objectives = [e[0] for e in expressions]
        __ideal = [e[1] for e in expressions]
        __nadir = [e[2] for e in expressions]
        self.__symbols = symbols
        super().__init__(
            nobj=__nobj,
            ideal=__ideal,
            nadir=__nadir,)

    def evaluate(self, population):
        for values in population:
            sdict = dict(zip((key for key in symbols), values))
            print(sdict)
            res = list(map(lambda obj: obj(sdict), self.__objectives))

            return res


class NautilusView():
    """A base class for creating views for the NAUTILUS-family methods
    defined in DESDEO.

    """
    def __init__(self,
                 method="ENAUTILUS",
                 optimizer="SciPyDE",
                 problem="River Pollution"
                 ):
        """Initializer

        :param method: Name of the method to be used. Must be defined in
        available_methods_d
        :param optimizer: Optimizer routine. Must be defined in
        available_optimizers_d
        :param problem: Pre-set or custom problem. Pre-sets must be defined in
        problems_d.

        """
        _method = m.available_methods_d[method]
        _optimizer = m.available_optimizers_d[optimizer]
        _problem = m.problems_d[problem]

        self.__method = _method(_problem, _optimizer)
        self.__nadir = self.method.problem.nadir
        self.__ideal = self.method.problem.ideal
        self.__initialized = False
        self.__template_dir = method + '/'
        self.__is_first_iteration = True
        self.__initialization_requirements = None
        self.__preference_requirements = None
        self.__last_iteration = None
        self.__help = None

    @property
    def method(self):
        return self.__method

    @property
    def nadir(self):
        return self.__nadir

    @nadir.setter
    def nadir(self, val):
        self.__nadir = val

    @property
    def ideal(self):
        return self.__ideal

    @ideal.setter
    def ideal(self, val):
        self.__ideal = val

    @property
    def initialized(self):
        return self.__initialized

    @initialized.setter
    def initialized(self, val):
        self.__initialized = val

    @property
    def template_dir(self):
        return self.__template_dir

    @template_dir.setter
    def template_dir(self, val):
        self.__template_dir = val

    @property
    def is_first_iteration(self):
        return self.__is_first_iteration

    @is_first_iteration.setter
    def is_first_iteration(self, val):
        self.__is_first_iteration = val

    @property
    def initialization_requirements(self):
        return self.__initialization_requirements

    @initialization_requirements.setter
    def initialization_requirements(self, val):
        self.__initialization_requirements = val

    @property
    def preference_requirements(self):
        return self.__preference_requirements

    @preference_requirements.setter
    def preference_requirements(self, val):
        self.__preference_requirements = val

    @property
    def last_iteration(self):
        return self.__last_iteration

    @last_iteration.setter
    def last_iteration(self, val):
        self.__last_iteration = val

    @property
    def help(self):
        return self.__help

    @help.setter
    def help(self, val):
        self.__help = val


class ENautilusView(NautilusView):
    """Specialization of the NautilusView class for the Enhanced NAUTILUS method.

    """
    def __init__(self,
                 method="ENAUTILUS",
                 optimizer="SciPyDE",
                 problem="River Pollution"
                 ):

        super().__init__(method, optimizer, problem)
        self.__user_iters = 5
        self.__current_iter = self.user_iters
        self.__n_generated_points = 10
        self.is_first_iteration = True
        self.initialization_requirements = [
            "User iterations",
            "Number of generated points",
            ]
        self.preference_requirements = [
            "Most preferred point",
            ]
        self.last_iteration = None
        self.__total_points_returned = 0
        self.help = {
            "name": "NAUTILUS Enhanced",
            "description": "NAUTILUS enhanced iterates a presolved problem "
            "starting from the nadir point. During each iteration, the "
            "decision maker is shown a set of points from which they must "
            "select the most preferred one. Using the selected points, a new "
            "set of points is calculated and the decision maker is asked once "
            "again to select their most preferred point. This is repeated "
            "unstil a solution on the pareto optimal front in reached."
        }

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

    def __validate_is_positive(self, val):
        if val < 1:
            raise ValueError("Value must be positive!")

    def initialize(self, **kwargs):
        if kwargs:
            self.user_iters = int(kwargs["User iterations"])
            self.current_iter = self.user_iters
            self.n_generated_points = int(kwargs["Number of generated points"])

        self.method.user_iters = self.user_iters
        self.method.current_iter = self.user_iters
        self.method.Ns = self.n_generated_points

        self.initialized = True

    def iterate(self, preference=(None, None)):
        """Iterate and return the results in a format that can be shown to the
        DM."""
        # Update the first iteration flag when an iteration is issued
        # for the first time
        if self.is_first_iteration:
            self.is_first_iteration = False

        results = self.method.next_iteration(
            preference=preference)

        # The dictionary entry labeled by the preference requirements are posed
        # to the DM as choices. Alwats return the latest points.
        start = self.__total_points_returned
        results_d = {
            "Most preferred point": [entry[1] for entry in results[start:]],
            "lower_bounds": [entry[0] for entry in results[start:]],
            }
        self.last_iteration = results_d
        self.__total_points_returned = len(results)

        # Update the underlying method
        self.current_iter = self.method.current_iter

        return results_d


available_method_views_d = {
    "ENAUTILUS": ENautilusView,
    }


# TESTIN DELETE ME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


__example_valid = [
    {'expression': 'x + y + z', 'lower_bound': 0.0, 'upper_bound': 5.0},
    {'expression': 'x - z / y * 3', 'lower_bound': 33, 'upper_bound': 40.0},
    {'expression': '10 * x + 9', 'lower_bound': -1, 'upper_bound': 1},
    ]

expressions, symbols = parse(__example_valid)

anal = AnalyticalProblem(expressions, symbols)
print(anal.nof_objectives())
print(anal.evaluate([[1, 2, 3]]))
