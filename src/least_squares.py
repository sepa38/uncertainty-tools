from .uncertain_value import UncertainValue
from .array import Array


def least_squares(x, y):
    if not (isinstance(x, Array) and isinstance(y, Array)):
        raise TypeError("Both arrays must be instances of uncertain_tools.Array")
    if len(x) != len(y):
        raise ValueError("Both arrays must have the same length.")

    n = len(x)
    x_values = [x_uv.value for x_uv in x]
    y_values = [y_uv.value for y_uv in y]
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xx = sum(val**2 for val in x_values)
    sum_xy = sum(x_values[i] * y_values[i] for i in range(n))

    variance_x = (n * sum_xx - sum_x**2) / n
    a_value = (sum_xy - sum_x * sum_y / n) / variance_x
    b_value = (sum_y - a_value * sum_x) / n

    residuals = [(y_values[i] - (a_value * x_values[i] + b_value)) ** 2 for i in range(n)]
    residual_sum = sum(residuals)
    variance = residual_sum / (n - 2)

    a_error = (variance / variance_x) ** 0.5
    b_error = (variance * (1 / n + (sum_x / n)**2 / variance_x)) ** 0.5

    a = UncertainValue(a_value, a_error)
    b = UncertainValue(b_value, b_error)

    return a, b
