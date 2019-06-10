from functools import reduce

from django.test import TestCase, tag
from .stateful_view import ENautilusView, NautilusView
from .expression_parser import exprs_to_lambda, free_symbols_dict


@tag("stateful_view")
class NautilusView_test(TestCase):
    def test_initializer(self):
        # default values
        c = NautilusView()
        self.assertFalse(c.initialized)
        self.assertEqual(c.template_dir, "ENAUTILUS/")
        self.assertTrue(c.is_first_iteration)
        self.assertIsNone(c.initialization_requirements)
        self.assertIsNone(c.preference_requirements)
        self.assertIsNone(c.last_iteration)

    def test_properties(self):
        c = NautilusView()

        # nadir
        c.nadir = [2.0, 5.0]
        self.assertAlmostEqual(c.nadir, [2.0, 5.0])

        # ideal
        c.ideal = [5.5, -2.1]
        self.assertAlmostEqual(c.ideal, [5.5, -2.1])

        # initialized
        c.initialized = True
        self.assertTrue(c.initialized)

        # template_dir
        c.template_dir = "/test/path/alpha"
        self.assertEqual(c.template_dir, "/test/path/alpha")

        # is_first_iteration
        c.is_first_iteration = False
        self.assertFalse(c.is_first_iteration)

        # initialization_requirements
        c.initialization_requirements = ["nadir", "iters"]
        self.assertEqual(c.initialization_requirements, ["nadir", "iters"])

        # preference_requirements
        c.preference_requirements = ["best", "worst"]
        self.assertEqual(c.preference_requirements, ["best", "worst"])

        # last_iteration
        c.last_iteration = [5.0, 2.0, -3.33]
        self.assertAlmostEqual(c.last_iteration, [5.0, 2.0, -3.33])


class ENautilusView_test(TestCase):
    def test_setters_and_getters(self):
        # user_iters
        c = ENautilusView()
        self.assertEqual(c.user_iters, 5)
        c.user_iters = 10
        self.assertEqual(c.user_iters, 10)

        # current_iter
        c = ENautilusView()
        self.assertEqual(c.current_iter, 5)
        c.current_iter = 10
        self.assertEqual(c.current_iter, 10)

        # n_generated_points
        c = ENautilusView()
        self.assertEqual(c.n_generated_points, 10)
        c.n_generated_points = 15
        self.assertEqual(c.n_generated_points, 15)

    def test_setters_bad_value(self):
        c = ENautilusView()

        with self.assertRaises(ValueError):
            c.user_iters = -1

        with self.assertRaises(ValueError):
            c.current_iter = -1

        with self.assertRaises(ValueError):
            c.n_generated_points = -1

    def test_initialization(self):
        c = ENautilusView()

        # Check default vals before initialization
        self.assertFalse(c.initialized)
        self.assertEqual(c.user_iters, 5)
        self.assertEqual(c.n_generated_points, 10)
        self.assertTrue(c.is_first_iteration)

        # Check values after initialization
        vals = {"User iterations": 15, "Number of generated points": 20}
        c.initialize(**vals)
        self.assertTrue(c.initialized)
        self.assertEqual(c.user_iters, 15)
        self.assertEqual(c.n_generated_points, 20)

        # Check that the underlying method has also been initialized
        self.assertEqual(c.method.user_iters, 15)
        self.assertEqual(c.method.Ns, 20)

        # Check that missing keys are noted
        missing_vals = {"False key": "adsfdfa"}
        with self.assertRaises(KeyError):
            c.initialize(**missing_vals)

    def test_iterate(self):
        c = ENautilusView()

        # Check decrement of current iter after iteration
        vals = {"User iterations": 10, "Number of generated points": 10}
        c.initialize(**vals)
        self.assertEqual(c.current_iter, 10)
        self.assertTrue(c.is_first_iteration)
        c.iterate()
        self.assertEqual(c.current_iter, 9)
        self.assertFalse(c.is_first_iteration)

    def test_last_iteration(self):
        c = ENautilusView()
        c.initialize()
        curr = c.iterate()
        last = c.last_iteration
        self.assertTrue(compare_dicts(curr, last))
        curr = c.iterate((last["Most preferred point"][0],
                          last["lower_bounds"][0]))
        self.assertFalse(compare_dicts(curr, last))


@tag("stateful_view")
def compare_dicts(this, that):
    eps = 0.001
    ress = []
    for key in this.keys():
        for vals1, vals2 in zip(this[key], that[key]):
            res = [eps > abs(v1 - v2) for (v1, v2) in zip(vals1, vals2)]
            ress.append(reduce(lambda x, y: x and y, res))
    # True is all entries are True, otherwise, False
    return reduce(lambda x, y: x and y, ress)


@tag("parser")
class expression_parser_test(TestCase):
    def test_exprs_to_lambda(self):
        """Test that a simple string is properly parsed into a callable expression.
        """
        str_input = "x + y"
        lam = exprs_to_lambda(str_input)
        self.assertAlmostEqual(lam(5, 6), 11)

    def test_free_symbols_dict(self):
        """Test that the right free symbols are extracted from a simple string input.
        """
        str_input = "x - y / z"
        sdict = free_symbols_dict(str_input)
        lam = exprs_to_lambda(str_input)
        sdict["x"] = 5
        sdict["y"] = 7
        sdict["z"] = 13
        self.assertAlmostEqual(lam(**sdict), 4.46153846154)

    def test_exprs_to_lambda_complex(self):
        """A more complex test"""
        str_input = "cos(x*pi) + x**2 - y / sqrt(z) + a*y"
        sdict = free_symbols_dict(str_input)
        lam = (exprs_to_lambda(str_input))
        sdict["x"] = -5.1
        sdict["y"] = 1.2
        sdict["z"] = 9.3
        sdict["a"] = -0.004
        self.assertAlmostEqual(lam(**sdict), 24.66064798223447)
