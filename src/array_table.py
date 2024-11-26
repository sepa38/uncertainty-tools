from .uncertain_value import UncertainValue
from .array import Array


class ArrayTable:
    def __init__(self, data=None):
        self.columns = {}
        if data:
            for col, values in data.items():
                self.add_column(col, values)

    def add_column(self, name, values):
        if not isinstance(values, Array):
            values = Array(values)
        if self.columns and len(values) != len(self):
            raise ValueError("Columns must have the same number of rows.")
        self.columns[name] = values

    def __len__(self):
        if not self.columns:
            return 0
        return len(next(iter(self.columns.values())))

    def __getitem__(self, name):
        return self.columns[name]

    def __setitem__(self, name, values):
        self.add_column(name, values)

