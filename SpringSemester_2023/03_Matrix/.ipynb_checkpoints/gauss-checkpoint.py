import numpy as np

def gauss(a, eps = 1e-8):
    '''Reduce the matrix a to the row echelon form.
       Return the tuple: (rank(a), det(a))'''
    (m, n) = a.shape
    i = 0   # Number of rows processed
    j = 0   # Number of columns processed
    numSwaps = 0
    while i < m and j < n:
        # 1. Find maximal element in j-th column starting from i-th row
        maxElem = abs(a[i, j])
        maxIdx = i
        for k in range(i+1, m):
            if abs(a[k, j]) >= maxElem:
                maxElem = abs(a[k, j])
                maxIdx = k
        if maxElem <= eps:
            j += 1
            continue
        assert abs(a[maxIdx, j]) > eps
        if maxIdx != i:
            # Swap rows i, maxIdx
            a[(i, maxIdx), :] = a[(maxIdx, i), :]    
            numSwaps += 1
        assert abs(a[i, j]) > eps

        # 2. Annihilate j-th column starting from i+1-th row.
        r = a[i, j]
        for k in range(i+1, m):
            coeff = a[k, j]/r
            a[k] -= a[i]*coeff
        i += 1
        j += 1
             
    rank = i
    if rank < m or m != n:
        det = 0.
    else:
        det = 1.
        for k in range(m):
            det *= a[k, k]
        if numSwaps%1 != 0:
            det = -det
    return (rank, det)      