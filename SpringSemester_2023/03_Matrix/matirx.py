from gauss import gauss
import numpy as np

'''
# Test
a = np.array([[1,2,3],[4,5,6],[7,8,0]], dtype="float64")
b = np.array([2., 3., 5.])

# Test inverseMatrix function
print('inverseMatrix:\n', inverseMatrix(a))

# Test solveLinearSystem function
print('solveLinearSystem:\n', solveLinearSystem(a, b))
'''

def inverseMatrix(a):
    n = a.shape[0]
    a_inv = np.zeros((n, n))
    
    for i in range(n):
        e = np.zeros((n, 1))
        e[i] = 1
        a_inv[:, i] = solveLinearSystem(a, e).flatten()
    
    return a_inv

def solveLinearSystem(a, b):
    n = a.shape[0]
    ab = np.column_stack((a, b))  # Extended matrix
    
    for i in range(n):
        # Apply Gauss method to make the i-th diagonal element to 1
        # and all elements below it to 0
        ab[i] = ab[i] / ab[i, i]
        for j in range(i+1, n):
            ab[j] = ab[j] - ab[j, i]*ab[i]
    
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (ab[i, -1] - np.dot(ab[i, :-1], x)) / ab[i, i]
    
    return x
