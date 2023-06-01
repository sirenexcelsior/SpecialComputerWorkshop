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

Implement a Polynomial class representing an arbitrary degree polynomial with coefficients in the field of rational numbers. The operations of addition, multiplication, division with remainder, calculation of the greatest common divisor of a polynomial, derivation of a polynomial, and calculation of a polynomial with the same roots, free of multiple roots, i.e. quotient of polynomial $f$ divided by $gcd(f, f')$ should be implemented.
Note: In Python, rational numbers are represented by the class Fraction in the module fractions.

```python
>>> from fractions import *
>>> x = Fraction(3, 7)
>>> y = Fraction(1, 5)
>>> x + y
>>> Fraction(22, 35)
```

### 03_Matrix

There are 2 options in the task and one task is to be done. Students with odd numbers in the journal do problem 1, and students with even numbers do problem 2. In all the problems we need to implement a function which, depending on the variant, returns either a matrix or a linear array.
The problems assume that matrices and linear arrays are represented by numpy-arrays like numpy.ndarray. In all variants, use the already prepared function

`(rank, det) = gauss(a)`

which brings matrix a to a step form and returns matrix rank and determinant (for a non-square matrix the determinant is not calculated and returns 0). Matrix a is represented as a two-dimensional numpy array with real values. The function is implemented in the file "gauss.py".
Note again that the function should not print anything (and certainly should not enter anything from the keyboard!). The result of the function's work should be the calculation of the required object, which the function should return using the operator return. The initial arguments of the function should not be changed.

Calculate the inverse matrix to the nondegenerate square real matrix:

 `b = inverseMatrix(a)`

Solve a system of linear equations with a non-singular square real matrix:

`x = solveLinearSystem(a, b)`

Here $a$ is a matrix of real numbers, $b$ is an array of free terms of the equations. The function should return an array of x real numbers representing the solution of the system $a*x = b$.

### 04_RegressionProblem

Write, using the tkinter module, a window graphical application that illustrates the method of least squares. The user marks a set of points on the plane with the mouse, the program has to find a polynomial of a given degree that minimizes the sum of the squares of the deviations of the polynomial values from the values given by the interpolation nodes.

```python
!python LeastSquares.py
```

![LeastSquares](https://github.com/sirenexcelsior/SpecialComputerWorkshop/blob/main/README/Pic/LeastSquares.png)

### 05_MAE

Complete the program "[huberRegression.py](http://mech.math.msu.su/~vvb/Master/huberRegression.py)", which computes a linear regression using either the least squares method (i.e. minimising the quadratic error function of the MSE) or minimising the error function defined using the Huber function. Archive of all program files: "[huberRegression.zip](http://mech.math.msu.su/~vvb/Master/huberRegression.zip)". The program should additionally realize the third way of regression parameter calculation, which minimizes the mean value of absolute error MAE using linear programming methods. The modified program should look like this:

```python
!python HR.py
```

![HR](https://github.com/sirenexcelsior/SpecialComputerWorkshop/blob/main/README/Pic/HR.png)

### 06_Geometry

The solutions to all problems should be designed as functions in Sage (similar to functions in Python). For example, in the problem "Draw a triangle, an incircle and a Jergon point" the solution is presented as a function, which inputs 3 points and returns a graphical object.

Example solution of the problem: draw the triangle, the incircle and the circumcircle around it and also represent the process of their construction - the bisectors and the midpoint perpendiculars.
The code for the sage program is: "[geometry.sage](http://mech.math.msu.su/~vvb/Master/geometry.sage)".
Example of using the function:

```python
sage: load("geometry.sage")
sage: a = vector([0, 0]); b = vector([5, 1]); c = vector([3, 5])
sage: drawTriangle(a, b, c)
```

#### Gergon.sage

<img src="https://github.com/sirenexcelsior/SpecialComputerWorkshop/blob/main/README/Pic/Gergon.png?raw=true" alt="Gergon.png" style="zoom:50%;" />

#### Nagel.sage

<img src="https://github.com/sirenexcelsior/SpecialComputerWorkshop/blob/main/README/Pic/Nagel.png?raw=true" alt="Nagel.png" style="zoom:50%;" />

#### Lemoine.sage

<img src="https://github.com/sirenexcelsior/SpecialComputerWorkshop/blob/main/README/Pic/Lemoine.png?raw=true" alt="Lemoine.png" style="zoom:50%;" />
