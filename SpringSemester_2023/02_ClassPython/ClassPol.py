from fractions import Fraction
'''
    The ClassPol class represents a monic ClassPol. The coefficients of a ClassPol are stored by a list, where each element of the list represents the coefficient of the corresponding term and the position represents the number of times.
    
    For example, the ClassPol 1 + 2x + 3x^2 + 4x^3 + 5x^4 can be defined in the following way:
    
    p = ClassPol([1, 2, 3, 4, 5])
    
    This class supports the following operations:
    
    1. addition of ClassPols: p1 + p2
    2. subtraction of a ClassPol: p1 - p2
    3. multiplication of a ClassPol: p1 * p2
    4. division of ClassPols: p1 / p2
    5. finding the greatest common divisor of a ClassPol: ClassPol.gcd(p1, p2)
    6. find the derivative of a ClassPol: p.derivative()
    7. Simplify a ClassPol: p.simplify()

'''

class ClassPol:
    def __init__(self, coefficients):
        while len(coefficients) > 0 and coefficients[-1] == 0:
            coefficients.pop()  # remove zero coefficients from the end
        if len(coefficients) == 0:
            coefficients.append(0)  # at least one coefficient
        self.coefficients = [Fraction(c) for c in coefficients]

    def degree(self):
        return len(self.coefficients) - 1

    def __add__(self, other):
        if self.degree() < other.degree():
            return ClassPol([a + b for a, b in zip(self.coefficients, other.coefficients)] + other.coefficients[self.degree()+1:])
        else:
            return ClassPol([a + b for a, b in zip(self.coefficients, other.coefficients)] + self.coefficients[other.degree()+1:])

    def __sub__(self, other):
        if self.degree() < other.degree():
            return ClassPol([a - b for a, b in zip(self.coefficients, other.coefficients)] + [-b for b in other.coefficients[self.degree()+1:]])
        else:
            return ClassPol([a - b for a, b in zip(self.coefficients, other.coefficients)] + self.coefficients[other.degree()+1:])

    def __mul__(self, other):
        coeffs = [Fraction(0)] * (self.degree() + other.degree() + 1)
        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                coeffs[i + j] += a * b
        return ClassPol(coeffs)

    def __truediv__(self, other):
        if other.coefficients[-1] == 0:
            raise ValueError("Cannot divide by ClassPol with zero leading coefficient")
        result = [0]*(self.degree() - other.degree() + 1)
        divisor = other.coefficients[::-1]
        dividend = self.coefficients[::-1]
        for i in range(self.degree() - other.degree() + 1):
            result[i] = dividend[i] / divisor[0]
            for j in range(1, len(divisor)):
                dividend[i+j] -= result[i] * divisor[j]
        return ClassPol(result[::-1])

    def derivative(self):
        return ClassPol([i*c for i, c in enumerate(self.coefficients)][1:])

    @staticmethod
    def gcd(a, b):
        while b.degree() > 0:
            a, b = b, a - (a / b) * b
        return a

    def simplify(self):
        gcd = self.gcd(self, self.derivative())
        return self / gcd

    def __str__(self):
        return ' + '.join([f'{c}x^{i}' for i, c in enumerate(self.coefficients)])
