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


def weighted_least_squres(x, y, weights=None):
    if not (isinstance(x, Array) and isinstance(y, Array)):
        raise TypeError("Both arrays must be instances of uncertain_tools.Array")
    if len(x) != len(y):
        raise ValueError("Both arrays must have the same length.")

    min_error = min(y_uv.error for y_uv in y.values)
    min_error = min_error if min_error != 0 else 1

    n = len(x)
    x_values = [x_uv.value for x_uv in x.values]
    y_values = [y_uv.value for y_uv in y.values]

    y_errors = [y_uv.error if y_uv.error != 0 else min_error / 2 for y_uv in y.values]
    weights = [1 / y_error**2 for y_error in y_errors]

    sum_w = sum(weights)
    sum_wx = sum(weights[i] * x_values[i] for i in range(len(n)))
    sum_wy = sum(weights[i] * y_values[i] for i in range(len(n)))
    sum_wxx = sum(weights[i] * x_values[i]**2 for i in range(len(n)))
    sum_wxy = sum(weights[i] * x_values[i] * y_values[i] for i in range(len(n)))

    a_value = (sum_w * sum_wxy - sum_wx * sum_wy) / (sum_w * sum_wxx - sum_wx**2)
    b_value = (sum_wy - a * sum_wx) / sum_w

    a_error = (sum_w / (sum_w * sum_wxx - sum_wx**2)) ** 0.5
    b_error = (sum_wxx / (sum_w * sum_wxx - sum_wx**2)) ** 0.5

    a = UncertainValue(a_value, a_error)
    b = UncertainValue(b_value, b_error)

    return a, b
