import math


class UncertainValue:
    def __init__(self, value, error=0):
        self.value = value
        self.error = abs(error)

    def rounded(self):
        def exact_round(value, digit):
            if digit < 0:
                value = int(value)
                value_str = str(value)

                if -digit > len(value_str):
                    return 0

                rounded_value = int(value_str[:digit] + "0"*(-digit))
                round_up = 1 if int(value_str[digit]) >= 5 else 0
                if value < 0:
                    round_up *= -1
                rounded_value += round_up * pow(10, -digit)
                return rounded_value
            else:
                value = float(value)
                value_str = f"{value:.{digit+1}f}"
                integer_part, decimal_part = value_str.split(".")

                if digit >= len(decimal_part):
                    return value

                rounded_value = float(f"{integer_part}.{decimal_part[:digit]}")
                round_up = 1 if int(decimal_part[digit]) >= 5 else 0
                if value < 0:
                    round_up *= -1
                rounded_value += round_up * pow(10, -digit)

                if digit == 0:
                    rounded_value = int(rounded_value)
                return rounded_value

        if self.error == 0:
            return self

        error_str = f"{self.error:.1e}"
        error_parts = error_str.split('e')
        significant_digit = float(error_parts[0])
        exponent = int(error_parts[1])

        rounded_error = exact_round(significant_digit * 10**exponent, -exponent)
        rounding_digit = -int(f"{rounded_error:.1e}".split('e')[1])
        rounded_value = exact_round(self.value, rounding_digit)

        if rounded_error >= 1:
            rounded_value = int(rounded_value)
            rounded_error = int(rounded_error)

        return UncertainValue(rounded_value, rounded_error)

    def format_value_and_error(self):
        rounded_instance = self.rounded()
        error_decimal_places = -int(f"{rounded_instance.error:.1e}".split('e')[1])
        if error_decimal_places > 0:
            value_str = f"{rounded_instance.value:.{error_decimal_places}f}"
            error_str = f"{rounded_instance.error:.{error_decimal_places}f}"
        else:
            value_str = str(rounded_instance.value)
            error_str = str(rounded_instance.error)
        return value_str, error_str

    def sqrt(self):
        if self.value < 0:
            raise ValueError("Cannot take the square root of a negative value.")

        new_value = self.value ** 0.5
        new_error = (self.error / (2 * new_value))
        return UncertainValue(new_value, new_error)

    def log(self, base=math.e):
        if self.value <= 0:
            raise ValueError("Cannot take the logarithm of a non-positive value.")

        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1.")

        new_value = math.log(self.value) / math.log(base)
        new_error = self.error / (self.value * math.log(base))
        return UncertainValue(new_value, new_error)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = UncertainValue(other, 0)
        if isinstance(other, UncertainValue):
            new_value = self.value + other.value
            new_error = (self.error**2 + other.error**2) ** 0.5
            return UncertainValue(new_value, new_error)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = UncertainValue(other, 0)
        if isinstance(other, UncertainValue):
            new_value = self.value - other.value
            new_error = (self.error**2 + other.error**2) ** 0.5
            return UncertainValue(new_value, new_error)
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
            return UncertainValue(new_value, new_error)
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
            return UncertainValue(new_value, new_error)
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
        return UncertainValue(new_value, new_error)

    def __neg__(self):
        return UncertainValue(-self.value, self.error)

    def __abs__(self):
        return UncertainValue(abs(self.value), self.error)

    def __repr__(self):
        value_str, error_str = self.format_value_and_error()
        if self.error == 0:
            if int(float(value_str)) == float(value_str):
                value_str = value_str.split(".")[0]
            return value_str
        return f"{value_str} ± {error_str}"

    def to_latex(self):
        rounded_instance = self.rounded()
        value_str, error_str = rounded_instance.format_value_and_error()
        if self.error == 0:
            if int(float(value_str)) == float(value_str):
                value_str = value_str.split(".")[0]
            return f"${value_str}$"
        return f"${value_str} \pm {error_str}$"
