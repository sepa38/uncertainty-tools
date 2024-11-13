from .uncertain_value import UncertainValue

class Array:
    def __init__(self, values=[]):
        if not isinstance(values, list):
            raise ValueError("Values must be a list.")

        if not all(isinstance(v, (UncertainValue, int, float)) for v in values):
            raise ValueError("All elements must be instances of UncertainValue, int or float.")

        self.values = [v if isinstance(v, UncertainValue) else UncertainValue(v) for v in values]

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Array(self.values[index.start:index.stop:index.step])
        else:
            return self.values[index]

    def __setitem__(self, index, value):
        if isinstance(value, (UncertainValue, int, float)):
            value = value if isinstance(value, UncertainValue) else UncertainValue(value)
            self.values[index] = value
        else:
            raise ValueError("Element must be an instance of UncertainValue, int or float")

    def __repr__(self):
        return f"Array({self.values})"

    def __add__(self, other):
        if not isinstance(other, Array):
            raise ValueError("Operand must be an instance of Array.")
        if len(self) != len(other):
            raise ValueError("Arrays must have the same length.")
        return Array([self[i] + other[i] for i in range(len(self))])

    def __sub__(self, other):
        if not isinstance(other, Array):
            raise ValueError("Operand must be an instance of Array.")
        if len(self) != len(other):
            raise ValueError("Arrays must have the same length.")
        return Array([self[i] - other[i] for i in range(len(self))])

    def __mul__(self, other):
        if not isinstance(other, Array):
            raise ValueError("Operand must be an instance of Array.")
        if len(self) != len(other):
            raise ValueError("Arrays must have the same length.")
        return Array([self[i] * other[i] for i in range(len(self))])

    def __truediv__(self, other):
        if not isinstance(other, Array):
            raise ValueError("Operand must be an instance of Array.")
        if len(self) != len(other):
            raise ValueError("Arrays must have the same length.")
        return Array([self[i] / other[i] for i in range(len(self))])

    def append(self, value):
        if isinstance(value, (UncertainValue, int, float)):
            value = value if isinstance(value, UncertainValue) else UncertainValue(value)
            self.values.append(value)
        else:
            raise ValueError("Appended value must be an instance of UncertainValue, int or float.")
