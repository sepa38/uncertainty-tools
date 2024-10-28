import math


class UncertainValue:
    def __init__(self, value, error=0):
        self.value = value
        self.error = error

    def round_to_significant(self, value, error):
        if error == 0:
            return value, error

        error_str = f"{error:.1e}"
        error_parts = error_str.split('e')
        significant_digit = float(error_parts[0])
        exponent = int(error_parts[1])

        rounded_error = round(significant_digit*pow(10, exponent), -exponent)
        rounding_digit = int(f"{rounded_error:.1e}".split('e')[1])
        rounded_value = round(value, -rounding_digit)

        if rounded_error >= 1:
            rounded_value = int(rounded_value)
            rounded_error = int(rounded_error)

        return rounded_value, rounded_error

    def sqrt(self):
        if self.value < 0:
            raise ValueError("Cannot take the square root of a negative value.")

        new_value = self.value ** 0.5
        new_error = (self.error / (2 * new_value))
        rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
        return UncertainValue(rounded_value, rounded_error)

    def log(self, base=math.e):
        if self.value <= 0:
            raise ValueError("Cannot take the logarithm of a non-positive value.")

        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1.")

        new_value = math.log(self.value) / math.log(base)
        new_error = self.error / (self.value * math.log(base))
        rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
        return UncertainValue(rounded_value, rounded_error)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = UncertainValue(other, 0)
        if isinstance(other, UncertainValue):
            new_value = self.value + other.value
            new_error = (self.error**2 + other.error**2) ** 0.5
            rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
            return UncertainValue(rounded_value, rounded_error)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = UncertainValue(other, 0)
        if isinstance(other, UncertainValue):
            new_value = self.value - other.value
            new_error = (self.error**2 + other.error**2) ** 0.5
            rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
            return UncertainValue(rounded_value, rounded_error)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            other = UncertainValue(other, 0)
        return other.__sub__(self)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = UncertainValue(other, 0)
        if isinstance(other, UncertainValue):
            new_value = self.value * other.value
            partial_x1 = other.value
            partial_x2 = self.value
            new_error = ((partial_x1 * self.error)**2 + (partial_x2 * other.error)**2) ** 0.5
            rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
            return UncertainValue(rounded_value, rounded_error)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = UncertainValue(other, 0)
        if isinstance(other, UncertainValue):
            if other.value == 0:
                raise ZeroDivisionError("Cannot divide by zero.")

            new_value = self.value / other.value
            partial_x1 = 1 / other.value
            partial_x2 = -self.value / (other.value**2)
            new_error = ((partial_x1 * self.error)**2 + (partial_x2 * other.error)**2) ** 0.5
            rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
            return UncertainValue(rounded_value, rounded_error)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            other = UncertainValue(other, 0)
        return other.__truediv__(self)

    def __pow__(self, exponent):
        if self.value < 0 and exponent % 1 != 0:
            raise ValueError("Cannot raise a negative base to a non-integer exponent.")

        new_value = pow(self.value, exponent)
        new_error = abs(exponent * new_value / self.value * self.error)
        rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
        return UncertainValue(rounded_value, rounded_error)

    def __repr__(self):
        return f"{self.value} ± {self.error}"
