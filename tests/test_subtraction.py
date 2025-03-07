import unittest
import sys
import os

sys.path.append(os.pardir)

from src import UncertainValue


class TestUncertainValueSubtraction(unittest.TestCase):
    def test_substraction_both_uncertain(self):
        x1 = UncertainValue(15.0, 0.5)
        x2 = UncertainValue(10.0, 0.3)
        result = x1 - x2
        self.assertEqual(repr(result), "5.0 ± 0.6")

    def test_subtraction_one_uncertain_zero_error(self):
        x1 = UncertainValue(20.0, 0)
        x2 = UncertainValue(10.0, 0.5)
        result = x1 - x2
        self.assertEqual(repr(result), "10.0 ± 0.5")

    def test_subtraction_with_constant(self):
        x1 = UncertainValue(10, 0.5)
        result = x1 - 5
        self.assertEqual(repr(result), "5.0 ± 0.5")

        result = 15 - x1
        self.assertEqual(repr(result), "5.0 ± 0.5")

    def test_subtraction_with_negative_values(self):
        x1 = UncertainValue(-20, 0.5)
        x2 = UncertainValue(-10, 0.3)
        result = x1 - x2
        self.assertEqual(repr(result), "-10.0 ± 0.6")

    def test_subtraction_large_value_small_error(self):
        x1 = UncertainValue(2e6, 1)
        x2 = UncertainValue(1e6, 2)
        result = x1 - x2
        self.assertEqual(repr(result), "1000000 ± 2")

    def test_substraction_large_value_difference(self):
        x1 = UncertainValue(1e6, 1e-3)
        x2 = UncertainValue(1e-2, 1e-3)
        result = x1 - x2
        self.assertEqual(repr(result), "999999.990 ± 0.001")

    def test_substraction_large_error_difference(self):
        x1 = UncertainValue(20, 5)
        x2 = UncertainValue(10, 1e-3)
        result = x1 - x2
        self.assertEqual(repr(result), "10 ± 5")


if __name__ == "__main__":
    unittest.main()
