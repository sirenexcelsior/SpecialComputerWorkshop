# SpecialComputerWorkshop
SpecialComputerWorkshop

## Overview
This is a code repository for homework on a special course in computing for the Master's degree in Mathematics at Moscow State University. The course is taught by Vladimir Borisenko. Homework web address: [~vvb/Master](http://mech.math.msu.su/~vvb/Master/index.html)

## SpringSemester_2023

### 01_NumberTheory

1. Implement the Miller-Rabin probabilistic simplicity test.
2. Implement an algorithm for the Chinese remainder theorem.
3. Factorize an integer using Pollard's $ρ$-algorithm.
4. Factorize an integer using Pollard's $p-1$ algorithm.
5. Calculate the square root of x in the field $Z_p$ ($p$ is prime), i.e. find $r$ such that $r_2 ≡ x (mod p)$.

### 02_ClassPython

Implement a Polynomial class representing an arbitrary degree polynomial with coefficients in the field of rational numbers. The operations of addition, multiplication, division with remainder, calculation of the greatest common divisor of a polynomial, derivation of a polynomial, and calculation of a polynomial with the same roots, free of multiple roots, i.e. quotient of polynomial f divided by $gcd(f, f')$ should be implemented.
Note: In Python, rational numbers are represented by the class Fraction in the module fractions.

```python
>>> from fractions import *
>>> x = Fraction(3, 7)
>>> y = Fraction(1, 5)
>>> x + y
>>> Fraction(22, 35)
```

