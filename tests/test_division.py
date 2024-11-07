import unittest
import sys
import os
sys.path.append(os.pardir)

from uncertain_value import UncertainValue # type: ignore


class TestUncertainValueDivision(unittest.TestCase):

    def test_division_both_uncertain(self):
        x1 = UncertainValue(20, 0.5)
        x2 = UncertainValue(10, 0.3)
        result = x1 / x2
        self.assertEqual(repr(result), "2.00 ± 0.08")

    def test_division_one_uncertain_zero_error(self):
        x1 = UncertainValue(10, 0.5)
        x2 = UncertainValue(20, 0)
        result = x1 / x2
        self.assertEqual(repr(result), "0.50 ± 0.03")

        result = x2 / x1
        self.assertEqual(repr(result), "2.0 ± 0.1")

    def test_division_with_constant(self):
        x1 = UncertainValue(10, 0.5)
        result = x1 / 5
        self.assertEqual(repr(result), "2.0 ± 0.1")

        result = 5 / x1
        self.assertEqual(repr(result), "0.50 ± 0.03")

    def test_division_with_negative_values(self):
        x1 = UncertainValue(-10, 0.6)
        x2 = UncertainValue(-20, 1)
        result = x1 / x2
        self.assertEqual(repr(result), "0.50 ± 0.04")

        x1 = UncertainValue(10, 0.6)
        x2 = UncertainValue(-20, 1)
        result = x1 / x2
        self.assertEqual(repr(result), "-0.50 ± 0.04")

        x1 = UncertainValue(-10, 0.6)
        x2 = UncertainValue(20, 1)
        result = x1 / x2
        self.assertEqual(repr(result), "-0.50 ± 0.04")

    def test_division_large_value_small_error(self):
        x1 = UncertainValue(1e6, 1)
        x2 = UncertainValue(2e6, 2)
        result = x1 / x2
        self.assertEqual(repr(result), "0.5000000 ± 0.0000007")

    def test_division_large_value_difference(self):
        x1 = UncertainValue(1e-2, 1e-4)
        x2 = UncertainValue(2e6, 1e-3)
        result = x1 / x2
        self.assertEqual(repr(result), "0.00000000500 ± 0.00000000005")

        result = x2 / x1
        self.assertEqual(repr(result), "200000000 ± 2000000")

    def test_division_large_error_difference(self):
        x1 = UncertainValue(10, 1e-3)
        x2 = UncertainValue(20, 5)
        result = x1 / x2
        self.assertEqual(repr(result), "0.5 ± 0.1")

        result = x2 / x1
        self.assertEqual(repr(result), "2.0 ± 0.5")

if __name__ == '__main__':
    unittest.main()
