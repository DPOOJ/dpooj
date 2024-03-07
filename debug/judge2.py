from sympy import symbols
import sympy

x = symbols('x')

f = sympy.Function('f')("x**2")
expr = "+-x-+exp((+--0*exp(((+--0*exp((+22394))^+0)))^+0))*98439"
print(sympy.simplify(expr))