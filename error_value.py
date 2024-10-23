class ErrorValue:
    def __init__(self, value, error):
        self.value = value
        self.error = error

    def __add__(self, other):
        if isinstance(other, ErrorValue):
            new_value = self.value + other.value
            new_error = (self.error**2 + other.error**2) ** 0.5
            return ErrorValue(new_value, new_error)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, ErrorValue):
            new_value = self.value - other.value
            new_error = (self.error**2 + other.error**2) ** 0.5
            return ErrorValue(new_value, new_error)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, ErrorValue):
            new_value = self.value * other.value
            partial_x1 = other.value
            partial_x2 = self.value
            new_error = ((partial_x1 * self.error)**2 + (partial_x2 * other.error)**2) ** 0.5
            return ErrorValue(new_value, new_error)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, ErrorValue):
            new_value = self.value / other.value
            partial_x1 = 1 / other.value
            partial_x2 = -self.value / (other.value**2)
            new_error = ((partial_x1 * self.error)**2 + (partial_x2 * other.error)**2) ** 0.5
            return ErrorValue(new_value, new_error)
        return NotImplemented

    def __repr__(self):
        return f"{self.value} ± {self.error}"
