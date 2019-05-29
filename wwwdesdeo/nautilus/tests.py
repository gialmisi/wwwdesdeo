from django.test import TestCase
from .stateful_view import ENautilusView


class ENautilusView_test(TestCase):
    def test_setters_and_getters(self):
        # user_iters
        c = ENautilusView()
        self.assertEqual(c.user_iters, 5)
        c.user_iters = 10
        self.assertEqual(c.user_iters, 10)

        # current_iters
        c = ENautilusView()
        self.assertEqual(c.current_iters, 5)
        c.current_iters = 10
        self.assertEqual(c.current_iters, 10)

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
            c.current_iters = -1

        with self.assertRaises(ValueError):
            c.n_generated_points = -1
