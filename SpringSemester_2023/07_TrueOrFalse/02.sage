def Groebner_is(equations):
    # 定义多项式环
    R = PolynomialRing(QQ, 'x, y')
    x, y = R.gens()
    # 构造Groebner基
    I = ideal(equations)
    G = I.groebner_basis()
    return G == [1]