from desdeo.method import ENAUTILUS, NAUTILUSv1, NNAUTILUS
from desdeo.optimization import SciPyDE
from desdeo.problem.toy import RiverPollution


available_methods_d = {
    "NAUTILUSv1": NAUTILUSv1,
    "ENAUTILUS": ENAUTILUS,
    "NAUTILUS-NAVIGATOR": NNAUTILUS,
    }
available_methods = list(available_methods_d.keys())

available_optimizers_d = {
    "SciPyDE": SciPyDE,
    "None": None,
    }
available_optimizers = list(
    available_optimizers_d.keys())

problems_d = {
    "Custom": None,  # TODO implement me!
    "River Pollution": RiverPollution(),
    }
problems = list(problems_d.keys())
