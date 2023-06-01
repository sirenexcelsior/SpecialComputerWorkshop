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

def outcircle(a, b, c):
    ab = (b - a).normalized()
    ac = (c - a).normalized()
    bisa = ab + ac
    
    ab = (b - a).normalized()
    bc = (c - b).normalized()
    bisb = ab + bc    

    center = intersectLines(
        a, bisa,
        b, bisb
    )
    radius = distanceToLine(center, b, bc)
    
    return center, radius
    
'''Draw a triangle with inscribed and circum circles'''
def drawTriangle(a, b, c):
    inc = incircle(a, b, c)
    t = line([a, b, c, a], color="green")
    circ = circle(inc[0], inc[1], color="red")
    inCenter = point(inc[0], size=40, color="red")
    
    # A点对应的外切圆
    onc_a = outcircle(a, b, c)
    outCenter_a = point(onc_a[0], size=40, color="red")
    outcirc_a = circle(onc_a[0], onc_a[1], color="red")
    # 连线
    bc = b - c
    bc_normal = normal(bc)
    foot_bc = intersectLines(onc_a[0], bc_normal, b, bc)
    Foot_bc = point(foot_bc, size=40, color="red")
    T1 = line([foot_bc, a], color="red")
    OUTcirc_a = outCenter_a + outcirc_a + Foot_bc + T1
    
    # B点对应的外切圆
    onc_b = outcircle(b, a, c)
    outCenter_b = point(onc_b[0], size=40, color="red")
    outcirc_b = circle(onc_b[0], onc_b[1], color="red")
    # 连线
    ac = a - c
    ac_normal = normal(ac)
    foot_ac = intersectLines(onc_b[0], ac_normal, a, ac)
    Foot_ac = point(foot_ac, size=40, color="red")
    T2 = line([foot_ac, b], color="red")
    OUTcirc_b = outCenter_b + outcirc_b + Foot_ac + T2
    
    # C点对应的外切圆
    onc_c = outcircle(c, a, b)
    outCenter_c = point(onc_c[0], size=40, color="red")
    outcirc_c = circle(onc_c[0], onc_c[1], color="red")
    # 连线
    ab = a - b
    ab_normal = normal(ab)
    foot_ab = intersectLines(onc_c[0], ab_normal, a, ab)
    Foot_ab = point(foot_ab, size=40, color="red")
    T3 = line([foot_ab, c], color="red")
    OUTcirc_c = outCenter_c + outcirc_c + Foot_ab + T3
    
    OUTcirc = OUTcirc_a + OUTcirc_b + OUTcirc_c
    
    # Nagel点
    nagel = intersectLines(c, c-foot_ab, b, b-foot_ac)
    Nagel = point(nagel, size=40, color="red")
    
    # 各边的延长线
    tout_a1 = line([b, 2*b-a], color="blue")
    tout_a2 = line([c, 2*c-a], color="blue")
    tout_b1 = line([a, 2*a-b], color="blue")
    tout_b2 = line([c, 2*c-b], color="blue")
    tout_c1 = line([a, 2*a-c], color="blue")
    tout_c2 = line([b, 2*b-c], color="blue")
    
    tout = tout_a1 + tout_a2 + tout_b1 + tout_b2 + tout_c1 + tout_c2

    
    return (
        t + OUTcirc + tout + Nagel
    )
