import unittest
import sys
import os

sys.path.append(os.pardir)

from src import UncertainValue


class TestUncertainValueMultiplication(unittest.TestCase):
    def test_multiplication_both_uncertain(self):
        x1 = UncertainValue(10, 0.6)
        x2 = UncertainValue(20, 1)
        result = x1 * x2
        self.assertEqual(repr(result), "200 ± 20")

    def test_multiplication_one_uncertain_zero_error(self):
        x1 = UncertainValue(10, 0.5)
        x2 = UncertainValue(20, 0)
        result = x1 * x2
        self.assertEqual(repr(result), "200 ± 10")

    def test_multiplication_with_constant(self):
        x1 = UncertainValue(10, 0.5)
        result = x1 * 5
        self.assertEqual(repr(result), "50 ± 3")

        result = 5 * x1
        self.assertEqual(repr(result), "50 ± 3")

    def test_multiplication_with_negative_values(self):
        x1 = UncertainValue(-10, 0.6)
        x2 = UncertainValue(-20, 1)
        result = x1 * x2
        self.assertEqual(repr(result), "200 ± 20")

        x1 = UncertainValue(10, 0.6)
        x2 = UncertainValue(-20, 1)
        result = x1 * x2
        self.assertEqual(repr(result), "-200 ± 20")

        x1 = UncertainValue(-10, 0.6)
        x2 = UncertainValue(20, 1)
        result = x1 * x2
        self.assertEqual(repr(result), "-200 ± 20")

    def test_multiplication_with_large_values(self):
        x1 = UncertainValue(1e3, 1)
        x2 = UncertainValue(2e3, 2)
        result = x1 * x2
        self.assertEqual(repr(result), "2000000 ± 3000")

    def test_multiplication_large_value_difference(self):
        x1 = UncertainValue(1e-2, 1e-4)
        x2 = UncertainValue(1e6, 1)
        result = x1 * x2
        self.assertEqual(repr(result), "10000 ± 100")

    def test_multiplication_large_error_difference(self):
        x1 = UncertainValue(10, 1e-3)
        x2 = UncertainValue(20, 5)
        result = x1 * x2
        self.assertEqual(repr(result), "200 ± 50")


if __name__ == "__main__":
    unittest.main()
