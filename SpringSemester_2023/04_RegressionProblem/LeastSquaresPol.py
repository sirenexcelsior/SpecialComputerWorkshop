import numpy as np

def leastSquaresValue(coeffs, t):
    """
    Value of Least Squares polynomial in point t
    coeffs: Coefficients of Least Squares polynomial
    t: Point of interpolation
    """
    n = len(coeffs)
    x_power = np.array([t**i for i in range(n)])
    s = np.dot(coeffs, x_power)
    return s

def computeLeastSquaresPol(nodes, degree):
    """
    Compute the coefficients of Least Squares polynomial
    nodes: Nodes of interpolation: [(x0, y0), ..., (xn, yn)]
    degree: The degree of the polynomial
    Return:
    coeffs: Coefficients of Least Squares polynomial
    """
    n = len(nodes)  # Number of points
    X = np.zeros((n, degree+1))
    y = np.zeros((n, 1))

    for i in range(n):
        for j in range(degree+1):
            X[i, j] = nodes[i][0]**j
        y[i] = nodes[i][1]

    coeffs = np.linalg.lstsq(X, y, rcond=None)[0]

    return coeffs.flatten()
