from .uncertain_value import UncertainValue


class Array:
    def __init__(self, values=[], latex_label=None):
        if not isinstance(values, list):
            raise ValueError("Values must be a list.")

        if not all(isinstance(v, (UncertainValue, int, float)) for v in values):
            raise ValueError(
                "All elements must be instances of UncertainValue, int or float."
            )

        self.values = [
            v if isinstance(v, UncertainValue) else UncertainValue(v) for v in values
        ]
        self.latex_label = latex_label

    def rounded(self):
        return Array([self[i].rounded() for i in range(len(self))])

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Array(
                self.values[index.start : index.stop : index.step], self.latex_label
            )
        else:
            return self.values[index]

    def __setitem__(self, index, value):
        if isinstance(value, (UncertainValue, int, float)):
            value = (
                value if isinstance(value, UncertainValue) else UncertainValue(value)
            )
            self.values[index] = value
        else:
            raise ValueError(
                "Element must be an instance of UncertainValue, int or float"
            )

    def __repr__(self):
        return f"Array({self.values})"

    def __add__(self, other):
        if not isinstance(other, (Array, UncertainValue, int, float)):
            raise ValueError(
                "Operand must be an instance of Array, int, float or UncertainValue."
            )

        if isinstance(other, Array):
            if len(self) != len(other):
                raise ValueError("Arrays must have the same length.")
            return Array(
                [self[i] + other[i] for i in range(len(self))], self.latex_label
            )

        return Array([self[i] + other for i in range(len(self))], self.latex_label)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, (Array, UncertainValue, int, float)):
            raise ValueError(
                "Operand must be an instance of Array, int, float or UncertainValue."
            )

        if isinstance(other, Array):
            if len(self) != len(other):
                raise ValueError("Arrays must have the same length.")
            return Array(
                [self[i] - other[i] for i in range(len(self))], self.latex_label
            )

        return Array([self[i] - other for i in range(len(self))], self.latex_label)

    def __rsub__(self, other):
        if not isinstance(other, (int, float, UncertainValue)):
            raise ValueError(
                "Operand must be an instance of Array, int, float or UncertainValue."
            )
        return Array([other - self[i] for i in range(len(self))], self.latex_label)

    def __mul__(self, other):
        if not isinstance(other, (Array, UncertainValue, int, float)):
            raise ValueError(
                "Operand must be an instance of Array, int, float or UncertainValue."
            )

        if isinstance(other, Array):
            if len(self) != len(other):
                raise ValueError("Arrays must have the same length.")
            return Array(
                [self[i] * other[i] for i in range(len(self))], self.latex_label
            )

        return Array([self[i] * other for i in range(len(self))], self.latex_label)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, (Array, UncertainValue, int, float)):
            raise ValueError(
                "Operand must be an instance of Array, int, float or UncertainValue."
            )

        if isinstance(other, Array):
            if len(self) != len(other):
                raise ValueError("Arrays must have the same length.")
            return Array(
                [self[i] / other[i] for i in range(len(self))], self.latex_label
            )

        return Array([self[i] / other for i in range(len(self))], self.latex_label)

    def __rtruediv__(self, other):
        if not isinstance(other, (int, float, UncertainValue)):
            raise ValueError(
                "Operand must be an instance of Array, int, float or UncertainValue."
            )
        return Array([other / self[i] for i in range(len(self))], self.latex_label)

    def append(self, value):
        if isinstance(value, (UncertainValue, int, float)):
            value = (
                value if isinstance(value, UncertainValue) else UncertainValue(value)
            )
            self.values.append(value)
        else:
            raise ValueError(
                "Appended value must be an instance of UncertainValue, int or float."
            )

    def set_latex_label(self, latex_label):
        self.latex_label = latex_label

    def map(self, func):
        return Array([func(v) for v in self.values], self.latex_label)

    def filter(self, predicate):
        return Array([v for v in self.values if predicate(v)], self.latex_label)
