# 返回向量的法向量
def normal(v):
    return vector([-v[1], v[0]])
    
# 返回两条线的交点，(p0, v0, p1, v1) 线0的上的点和方向向量
def intersectLines(p0, v0, p1, v1):
    n = normal(v1)
    t = (p1 - p0)*n / (v0*n)
    q = p0 + v0*t
    return q
    
# 返回点到线的距离， (t, p, v) 点t, 线上的点p和方向向量v
def distanceToLine(t, p, v):
    n = normal(v).normalized()
    return abs((t - p)*n)

# 返回内切圆
def incircle(a, b, c):
    ab = (b - a).normalized()
    ac = (c - a).normalized()
    bisa = ab + ac
    
    ba = (a - b).normalized()
    bc = (c - b).normalized()
    bisb = ba + bc
    
    center = intersectLines(
        a, bisa,
        b, bisb
    )
    radius = distanceToLine(center, a, ab)
    
    # Compute bisectors
    bisector_a = intersectLines(
        a, bisa, b, c - b
    )
    bisector_b = intersectLines(
        b, bisb, c, a - c
    )    
    ca = (a - c).normalized()
    cb = (b - c).normalized()
    bisc = ca + cb
    bisector_c = intersectLines(
        c, bisc, a, b - a
    )
    bisectors = (bisector_a, bisector_b, bisector_c)
    
    return (center, radius, bisectors)

# 返回两个点的中点
def midpoint(p0, p1):
    return (p0 + p1)/2

def drawTriangle(a, b, c):
    Triangle = line([a, b, c, a], color="black")
    
    # 重心
    mid_a = midpoint(b, c)
    midline_a = line([a, mid_a], color="blue")
    mid_b = midpoint(a, c)
    midline_b = line([b, mid_b], color="blue")
    mid_c = midpoint(b, a)
    midline_c = line([c, mid_c], color="blue")
    
    midline_p = intersectLines(a, mid_a-a, b, mid_b-b)
    midline_P = point(midline_p, size=40, color="blue")
    
    midline = midline_a + midline_b + midline_c + midline_P
    
    # 内心
    center, radius, bisectors = incircle(a, b, c)
    centerline_A = intersectLines(a, center-a, b, b-c)
    centerline_B = intersectLines(b, center-b, a, a-c)
    centerline_C = intersectLines(c, center-c, b, b-a)
    
    centerline_a = line([a, centerline_A], color="green")
    centerline_b = line([b, centerline_B], color="green")
    centerline_c = line([c, centerline_C], color="green")
    
    centerline = centerline_a + centerline_b + centerline_c
    
    centerline_p = intersectLines(a, centerline_A-a, b, centerline_B-b)
    
    # 绘制Lemoine点
    Lemoine_p = centerline_p *2 - midline_p
    Lemoine_P = point(Lemoine_p, size=40, color="red")
    
    Lemoine_a = intersectLines(a, Lemoine_p-a, b, b-c)
    Lemoine_b = intersectLines(b, Lemoine_p-b, a, a-c)
    Lemoine_c = intersectLines(c, Lemoine_p-c, a, a-b)
    
    Lemoine_A = line([a, Lemoine_a], color="red")
    Lemoine_B = line([b, Lemoine_b], color="red")
    Lemoine_C = line([c, Lemoine_c], color="red")
    
    Lomonie = Lemoine_P + Lemoine_A + Lemoine_B + Lemoine_C
    
    return (
        Triangle + midline + centerline + Lomonie
    )