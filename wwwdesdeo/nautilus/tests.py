from django.test import TestCase
from .stateful_view import ENautilusView


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
        self.assertTrue(c.first_iteration)

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
        self.assertTrue(c.first_iteration)
        c.iterate()
        self.assertEqual(c.current_iter, 9)
        self.assertFalse(c.first_iteration)


# class Forms_test(TestCase):
#     def test_initialization_form(self):
#         f = forms.InitializationForm(models.available_methods,
#                                      models.available_optimizers,
#                                      models.examples)
#         self.assertEqual(f.fields["interactive_method"],
#                          models.available_methods)
#         self.assertEqual(f.fields["available_optimizers"],
#                          models.available_optimizers)
#         self.assertEqual(f.fields["examples"],
#                          models.examples)
