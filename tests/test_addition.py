import unittest
import sys
import os

sys.path.append(os.pardir)

from src import UncertainValue


class TestUncertainValueAddition(unittest.TestCase):
    def test_addition_both_uncertain(self):
        x1 = UncertainValue(10, 0.5)
        x2 = UncertainValue(20, 0.3)
        result = x1 + x2
        self.assertEqual(repr(result), "30.0 ± 0.6")

    def test_addition_one_uncertain_zero_error(self):
        x1 = UncertainValue(10, 0.5)
        x2 = UncertainValue(20, 0)
        result = x1 + x2
        self.assertEqual(repr(result), "30.0 ± 0.5")

    def test_addition_with_constant(self):
        x1 = UncertainValue(10, 0.5)
        result = x1 + 5
        self.assertEqual(repr(result), "15.0 ± 0.5")

        result = 5 + x1
        self.assertEqual(repr(result), "15.0 ± 0.5")

    def test_addition_with_negative_values(self):
        x1 = UncertainValue(-10, 0.5)
        x2 = UncertainValue(-20, 0.3)
        result = x1 + x2
        self.assertEqual(repr(result), "-30.0 ± 0.6")

    def test_addition_large_value_small_error(self):
        x1 = UncertainValue(1e6, 1)
        x2 = UncertainValue(2e6, 2)
        result = x1 + x2
        self.assertEqual(repr(result), "3000000 ± 2")

    def test_addition_large_value_difference(self):
        x1 = UncertainValue(1e-2, 1e-3)
        x2 = UncertainValue(1e6, 1e-3)
        result = x1 + x2
        self.assertEqual(repr(result), "1000000.010 ± 0.001")

    def test_addition_large_error_difference(self):
        x1 = UncertainValue(10, 1e-3)
        x2 = UncertainValue(20, 5)
        result = x1 + x2
        self.assertEqual(repr(result), "30 ± 5")


if __name__ == "__main__":
    unittest.main()
