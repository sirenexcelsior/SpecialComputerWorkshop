# 米勒-拉宾的概率简单性检验

import random

'''
示例：
>> from M_R import *
>> miller_rabin(n=102030, k=3)
>> False
'''

def miller_rabin(n, k):
    # 检查n是否是素数，k是测试的精度
    if n == 2 or n == 3:
        return True   # 2和3是素数
    if n <= 1 or n % 2 == 0:
        return False   # 所有小于等于1的整数都不是素数，偶数也不是素数

    # 找到n-1的因子2^s和d，其中d是奇数
    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # 进行k次测试
    for i in range(k):
        a = random.randint(2, n-2)   # 选择随机的底数a
        x = pow(a, d, n)   # 计算x = a^d mod n
        if x == 1 or x == n-1:
            continue   # 如果x等于1或n-1，则重试
        for j in range(s-1):
            x = pow(x, 2, n)   # 计算x = x^2 mod n
            if x == n-1:
                break   # 如果x等于n-1，则跳出循环
        else:
            return False   # 如果x不等于n-1，则n一定不是素数
    return True   # n可能是素数
