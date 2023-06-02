from gauss import gauss
import numpy as np

def gauss_jordan(a):

    rank, _ = gauss(a)
    
    (n, m) = a.shape
    for i in range(rank, 0, -1):
        a[i-1] = a[i-1] / a[i-1, i-1]
        for j in range(i-1):
            a[j] = a[j] - a[j, i-1] * a[i-1]
    
    return a

def inverseMatrix(a):
    n = len(a)
    assert len(a[0]) == n, "Matrix must be square."
    
    a_ext = np.hstack((a, np.eye(n)))
    a_ext = gauss_jordan(a_ext)
    
    return a_ext[:, n:]

def solveLinearSystem(a, b):
    n = len(a)
    assert len(a[0]) == n, "Matrix must be square."
    assert len(b) == n, "The size of b must match the size of a."
    
    a_ext = np.hstack((a, np.reshape(b, (n, 1))))
    a_ext = gauss_jordan(a_ext)
    
    return a_ext[:, -1]
