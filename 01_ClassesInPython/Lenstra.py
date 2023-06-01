from math import gcd
from random import randint

def lenstra(n, max_iterations=1000): # 定义 Lenstra 算法函数，n 为要分解的整数，max_iterations 为最大迭代次数
    if n % 2 == 0: # 如果 n 是偶数
        return 2 # 返回因子 2
    for _ in range(max_iterations): # 迭代 max_iterations 次
        a = randint(1, n - 1) # 随机生成 a
        b = randint(1, n - 1) # 随机生成 b
        x = randint(1, n - 1) # 随机生成 x
        y = (x * x * x + a * x + b) % n # 计算 y 的值
        p = gcd(y * y - (x * x * x + a * x + b), n) # 计算 p 的值，即 y^2 和 x^3+ax+b 在模 n 意义下的差的最大公约数
        if p > 1: # 如果 p 大于 1，则找到一个因子
            return p
    return None

def factors(n):
    factors = []
    while n > 1:
        factor = lenstra(n)
        if factor is None:
            factors.append(n)
            break
        factors.append(factor)
        n //= factor
    return factors

print(factors(int(input("Please enter an integer:"))))