from fractions import Fraction

'''
You can use this class in the following way:
>>> from Polynomial import Polynomial as Pol
You can define a polynomial by doing something like this:
>>> p1 = Pol([1, 2, 3, 4, 5, 6, 7, 8, 9]) --> x^8 + 2x^7 + 3x^6 + 4x^5 + 5x^4 + 6x^3 + 7x^2 + 8x + 9
>>> p2 = Pol([9, 8, 7, 6, 5, 4, 3, 2, 1]) --> 9x^8 + 8x^7 + 7x^6 + 6x^5 + 5x^4 + 4x^3 + 3x^2 + 2x + 1
>>> p3 = Pol([1, 0, 2, 1])                --> x^3 + 2x + 1
>>> p1 + p2                               --> Addition
>>> p1 - p2                               --> Subtraction
>>> p1 * p2                               --> Multiplication
>>> p1 // p2                              --> Division
>>> p1 % p2                               --> Mod
>>> Pol.diff(p1)                          --> Derivation
>>> Pol.sameroot(p3)                      --> Calculating the greatest common divisor of a polynomial

'''

class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = [Fraction(coef) for coef in coefficients]

    def __repr__(self):
        return self.__str__()    

    def __str__(self):
        terms = []
        for i, coef in enumerate(self.coefficients):
            power = len(self.coefficients) - i - 1
            if coef == 0:
                continue
            term = ""
            if coef < 0:
                term += "(-"
            if abs(coef) != 1 or power == 0:
                term += str(abs(coef))
            if power > 1:
                term += f"x^{power}"
            elif power == 1:
                term += "x"
            if coef < 0:
                term += ")"
            terms.append(term)
        return " + ".join(terms)

    def __add__(self, other):
        len_diff = len(self.coefficients) - len(other.coefficients)
        if len_diff > 0:
            new_coefficients = self.coefficients[:]
            for i in range(len(other.coefficients)):
                new_coefficients[i+len_diff] += other.coefficients[i]
        else:
            new_coefficients = other.coefficients[:]
            for i in range(len(self.coefficients)):
                new_coefficients[i-len_diff] += self.coefficients[i]
        return Polynomial(new_coefficients)

    def __sub__(self, other):
        len_diff = len(self.coefficients) - len(other.coefficients)
        if len_diff > 0:
            new_coefficients = self.coefficients[:]
            for i in range(len(other.coefficients)):
                new_coefficients[i+len_diff] -= other.coefficients[i]
        else:
            new_coefficients = [-coef for coef in other.coefficients]
            for i in range(len(self.coefficients)):
                new_coefficients[i-len_diff] += self.coefficients[i]
        return Polynomial(new_coefficients)

    def __mul__(self, other):
        new_coefficients = [0] * (len(self.coefficients) + len(other.coefficients) - 1)
        for i, coef1 in enumerate(self.coefficients):
            for j, coef2 in enumerate(other.coefficients):
                new_coefficients[i+j] += coef1 * coef2
        return Polynomial(new_coefficients)

    def __floordiv__(self, other):
        temp = self.coefficients[:]
        result = []
        while len(temp) >= len(other.coefficients):
            coef = temp[-1] / other.coefficients[-1]
            result = [coef] + result
            for i in range(1, len(other.coefficients) + 1):
                temp[-i] -= coef * other.coefficients[-i]
            temp.pop()
        return Polynomial(result)


    def __mod__(self, other):
        # Remainder of long division
        temp = self.coefficients[:]
        while len(temp) >= len(other.coefficients):
            if len(other.coefficients) == 0:
                raise ValueError("Division by zero polynomial")
            coef = temp[-1] / other.coefficients[-1]
            for i in range(1, len(other.coefficients) + 1):
                temp[-i] -= coef * other.coefficients[-i]
            temp.pop()
        return Polynomial(temp)

    @classmethod
    def diff(cls, poly):
        new_coefficients = [coef * i for i, coef in enumerate(poly.coefficients)][1:]
        return cls(new_coefficients)

    @classmethod
    def gcd(cls, a, b):
        while b and len(b.coefficients) != 0:
            a, b = b, a % b
        return a

    @classmethod
    def sameroot(cls, poly):
        poly_diff = cls.diff(poly)
        gcd = cls.gcd(poly, poly_diff)
        return poly // gcd