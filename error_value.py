class ErrorValue:
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
        rounded_value = round(value, -exponent)

        if rounded_error >= 1:
            rounded_value = int(rounded_value)
            rounded_error = int(rounded_error)

        return rounded_value, rounded_error

    def __add__(self, other):
        if isinstance(other, ErrorValue):
            new_value = self.value + other.value
            new_error = (self.error**2 + other.error**2) ** 0.5
            rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
            return ErrorValue(rounded_value, rounded_error)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, ErrorValue):
            new_value = self.value - other.value
            new_error = (self.error**2 + other.error**2) ** 0.5
            rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
            return ErrorValue(rounded_value, rounded_error)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, ErrorValue):
            new_value = self.value * other.value
            partial_x1 = other.value
            partial_x2 = self.value
            new_error = ((partial_x1 * self.error)**2 + (partial_x2 * other.error)**2) ** 0.5
            rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
            return ErrorValue(rounded_value, rounded_error)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, ErrorValue):
            new_value = self.value / other.value
            partial_x1 = 1 / other.value
            partial_x2 = -self.value / (other.value**2)
            new_error = ((partial_x1 * self.error)**2 + (partial_x2 * other.error)**2) ** 0.5
            rounded_value, rounded_error = self.round_to_significant(new_value, new_error)
            return ErrorValue(rounded_value, rounded_error)
        return NotImplemented

    def __repr__(self):
        return f"{self.value} ± {self.error}"
