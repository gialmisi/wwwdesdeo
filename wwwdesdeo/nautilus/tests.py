from django.test import TestCase
from .stateful_view import ENautilusView

import models
import forms


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

        # Check values after initialization
        c.initialize(15, 20)
        self.assertTrue(c.initialized)
        self.assertEqual(c.user_iters, 15)
        self.assertEqual(c.n_generated_points, 20)

        # Check that the underlying method has also been initialized
        self.assertEqual(c.method.user_iters, 15)
        self.assertEqual(c.method.Ns, 20)

    def test_iterate(self):
        c = ENautilusView()

        # Check decrement of current iter after iteration
        c.initialize(10, 10)
        self.assertEqual(c.current_iter, 10)
        c.iterate()
        self.assertEqual(c.current_iter, 9)


class Forms_test(TestCase):
    def test_initialization_form(self):
        f = forms.InitializationForm(models.available_methods,
                                     models.available_optimizers,
                                     models.examples)
        self.assertEqual(f.fields["available_methods"],
                         models.available_methods)
        self.assertEqual(f.fields["available_optimizers"],
                         models.available_optimizers)
        self.assertEqual(f.fields["examples"],
                         models.examples)
