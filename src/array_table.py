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

    def __repr__(self):
        if not self.columns:
            return "Empty ArrayTable"
        column_names = list(self.columns.keys())
        rows = zip(*[self.columns[col].values for col in column_names])
        header = " | ".join(column_names)
        str_rows = "\n".join(" | ".join(map(str, row)) for row in rows)
        return f"{header}\n" + "-" * len(header) + f"\n{str_rows}"

    def to_latex(self):
        if not self.columns:
            return "Empty ArrayTable"
        column_names = list(self.columns.keys())
        rows = zip(*[self.columns[col].values for col in column_names])
        header = " & ".join(column_names)
        str_rows = f" \\\\ \n".join(
            " & ".join(cell.to_latex() for cell in row)
            for row in rows)
        return f"{header} \\\\ \hline\n" + f"{str_rows}"
