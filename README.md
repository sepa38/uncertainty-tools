# UncertaintyTools

A Python library for managing uncertain values, performing calculations with arrays, and creating LaTeX-compatible tabular data.


## Features
### UncertainValue
- Represents numerical values with associated uncertainties.
- Supports standard mathematical operations (+, -, *, /, etc.) with error propagation.
- Features include:
  - LaTeX-compatible formatting for scientific documents.
  - Automatic rounding based on significant figures in the uncertainty.

**Behind the scenes: Error propagation** \
The propagation of errors is based on the following formula:

$$\Delta y = \sqrt{\sum_{i=1}^n \left(\frac{\partial f}{\partial x_i} \Delta x_i \right)^2}$$

Here, $y = f(x_1, x_2, \cdots , x_n)$ represents a function of variables $x_i$, and $\Delta x_i$ represents the uncertainties in these variables. The library automatically applies this formula during calculations.

### Array
- A wrapper class for numerical data with enhanced functionality.
- Allows element-wise operations between:
  - `Array`
  - Scalars (e.g., integers, floats)
  - `UncertainValue` instances

### ArrayTable
- A tabular data structure built with `Array` columns.
- Key features:
  - Easy column management (add, update, or remove columns).
  - Customizable LaTeX labels for columns.
  - Generates LaTeX-formatted tables for integration into documents.


## Usage Examples
### 1. `UncertainValue`
```python
# Create uncertain values
x = UncertainValue(250, 5)
y = UncertainValue(100, 4)

print(x + y) # 350 ± 6.4031242374328485
print(x - y) # 150 ± 6.4031242374328485
print(x * y) # 25000 ± 1118.033988749895
print(x / y) # 2.5 ± 0.1118033988749895
print((x / 3).rounded()) # 83 ± 2

# LaTeX formatting
print((x * y).to_latex()) # $25000 \pm 1000$
print((x * y).to_latex(scientific=True)) # $(2.5 \pm 0.1) \times 10^{4}$
```
The propagation of errors for operations such as addition, subtraction, multiplication, and division is calculated using the formula described in **Features**. For example:
- When multiplying $x = 250 \pm 5$ and $y = 100 \pm 4$, the result is $25000 \pm 1118.03$, where the uncertainty is calculated as:
$$\Delta z = \sqrt{
  \left(\frac{\partial f}{\partial x} \Delta x \right)^2 + 
  \left(\frac{\partial f}{\partial y} \Delta y \right)^2
}$$

### 2. `Array`
```python
# Create arrays
x = Array([UncertainValue(12.8, 0.8), UncertainValue(11.4, 0.6), UncertainValue(12.1, 0.7)])
y = Array([20, 18, 19])

# Operations
print(x + 2) # Array([14.8 ± 0.8, 13.4 ± 0.6, 14.1 ± 0.7])
print((x / y).rounded()) # Array([0.64 ± 0.04, 0.63 ± 0.03, 0.64 ± 0.04])
```

## 3. `ArrayTable`
```python
# Create data columns
V = Array([UncertainValue(12.8, 0.8), UncertainValue(11.4, 0.6), UncertainValue(12.1, 0.7)])
I = Array([20, 18, 19]) / 1000

# Create table
table = ArrayTable({"V": V, "I": I})
table["R"] = table["V"] / table["I"]

# View table
print(table)
# V | I | R
# ---------
# 12.8 ± 0.8 | 0.02 ± 0.0 | 640.0 ± 40.0
# 11.4 ± 0.6 | 0.018 ± 0.0 | 633.3333333333334 ± 33.333333333333336
# 12.1 ± 0.7 | 0.019 ± 0.0 | 636.8421052631579 ± 36.8421052631579

# Set LaTeX labels
table["V"].set_latex_label("$V / \\text{V}$")
table["I"].set_latex_label("$I / \\text{mA}$")
table["R"].set_latex_label("$R / \\Omega$")

# Generate LaTeX output
print(table.to_latex())
# $V / \text{V}$ & $I / \text{mA}$ & $R / \Omega$ \\ \hline
# $12.8 \pm 0.8$ & $0.02$ & $640 \pm 40$ \\ 
# $11.4 \pm 0.6$ & $0.018$ & $630 \pm 30$ \\ 
# $12.1 \pm 0.7$ & $0.019$ & $640 \pm 40$
```
