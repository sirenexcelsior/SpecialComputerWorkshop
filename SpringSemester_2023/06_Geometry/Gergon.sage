'''Normal to a vector'''
def normal(v):
    return vector([-v[1], v[0]])
    
'''Intersection of two straight lines.
Each line is defined by a point and a direction vector'''
def intersectLines(p0, v0, p1, v1):
    
    n = normal(v1)
    t = (p1 - p0)*n / (v0*n)
    q = p0 + v0*t
    return q
    
'''Distance from a point to a line'''
def distanceToLine(t, p, v):
    n = normal(v).normalized()
    return abs((t - p)*n)
    
'''Circle inscribed in a triangle.
Return center and radius of the circle and
3 points of bisectors'''
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
    
'''The circumcircle around a triangle'''
def circumcircle(a, b, c):
    mab = (a + b)*(1/2)
    mac = (a + c)*(1/2)
    nab = normal(b - a)
    nac = normal(c - a)
    center = intersectLines(
        mab, nab,
        mac, nac
    )
    radius = (a - center).norm()
    return (center, radius)

def intersec(a, b, c):
    # 计算内切圆的圆心坐标
    inc = incircle(a, b, c)
    center = inc[0]
    # 边AB的方向向量
    ab = b - a
    # 边BC的方向向量
    bc = c - b
    # 边CA的方向向量
    ca = a - c
    # 边AB的法向量
    ab_normal = normal(ab)
    # 边BC的法向量
    bc_normal = normal(bc)
    # 边CA的法向量
    ca_normal = normal(ca)    
    # 计算垂足的坐标
    foot_ab = intersectLines(center, ab_normal, a, ab)
    foot_bc = intersectLines(center, bc_normal, b, bc)
    foot_ca = intersectLines(center, ca_normal, c, ca)
    
    return foot_ab, foot_bc, foot_ca

'''Draw a triangle with inscribed and circum circles'''
def drawGergon(a, b, c):
    inc = incircle(a, b, c)
    t = line([a, b, c, a], color="black")
    circ = circle(inc[0], inc[1], color="red")
    inCenter = point(inc[0], size=40, color="red")
    
    foot_ab, foot_bc, foot_ca = intersec(a, b, c)
    Foot_ab = point(foot_ab, size=40, color="green")
    Foot_bc = point(foot_bc, size=40, color="green")
    Foot_ca = point(foot_ca, size=40, color="green")

    t1 = line([c, foot_ab], color="green")
    t2 = line([b, foot_ca], color="green")
    t3 = line([a, foot_bc], color="green")
    
    
    gergon = intersectLines(a, foot_bc-a, b, foot_ca-b)
    Gergon = point(gergon, size=40, color="green")
    
    return (
        t + t1 + t2 + t3 +
        circ + Foot_ab + Foot_bc + Foot_ca + Gergon
    )
