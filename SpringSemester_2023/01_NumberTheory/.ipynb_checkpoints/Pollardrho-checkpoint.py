from math import gcd
import random

'''
该代码实现了Pollard Rho算法来分解一个给定的正整数。
Pollard Rho算法是一种用于因数分解的随机算法，能够有效地分解大整数。
示例：
>> from Pollardrho import *
>> factors(102030)
>> [30, 179, 19]
'''

def pollard_rho(n):
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    g = 1

    while g == 1:
        x = ((x * x) % n + c) % n
        y = ((y * y) % n + c) % n
        y = ((y * y) % n + c) % n
        g = gcd(abs(x - y), n)

    return g

def factorize(n):
    if n == 1:
        return []
    if is_prime(n):
        return [n]
    
    p = pollard_rho(n)
    
    while p == n:
        p = pollard_rho(n)
        
    return factorize(p) + factorize(n // p)

def is_prime(n):
    if n <= 3:
        return True
    
    for i in range(5):
        a = random.randint(2, n - 2)
        
        if pow(a, n - 1, n) != 1:
            return False
        
    return True

def factors(n):
    factors = []
    while n > 1:
        factor = pollard_rho(n)
        if factor is None:
            factors.append(n)
            break
        factors.append(factor)
        n //= factor
    return factors
