def Ring_is(A, B):
    # 定义一个有理数域上的多项式环
    R = PolynomialRing(QQ, 'x,y,z')
    # 定义两个多项式集合

    # 定义两个理想，分别由两个多项式集合生成
    I = R.ideal(A)
    J = R.ideal(B)
    # 检查两个理想是否相等，即是否生成相同的仿射代数簇
    return I == J