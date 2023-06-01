'''Normal to a vector'''
def normal(v):
    return vector([-v[1], v[0]])
    
'''Intersection of two straight lines.
Each line is defined by a point and a direction vector'''
def intersectLines(p0, v0, p1, v1):
    # q = p0 + v0*t, t - a number
    # n = normal(v1)
    # (q - p1)*n = 0
    # (p0 + v0*t - p1)*n = 0
    # (v0*n)*t + (p0 - p1)*n = 0 
    # t = (p1 - p0)*n / (v0*n)

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

'''Draw a triangle with inscribed and circum circles'''
def drawTriangle(a, b, c):
    inc = incircle(a, b, c)
    t = line([a, b, c, a], color="blue")
    circ = circle(inc[0], inc[1], color="red")
    inCenter = point(inc[0], size=40, color="red")

    outc = circumcircle(a, b, c)
    outcirc = circle(outc[0], outc[1], color="green")
    outCenter = point(outc[0], size=40, color="green")

    bisectors = inc[2]
    bis = (
        line([a, bisectors[0]], color="red") + 
        line([b, bisectors[1]], color="red") + 
        line([c, bisectors[2]], color="red")
    )
    
    mab = (a + b)*(1/2)
    mbc = (b + c)*(1/2)
    mca = (c + a)*(1/2)
    perpediculars = (
        line([mab, outc[0]], color="green") +  
        line([mbc, outc[0]], color="green") +  
        line([mca, outc[0]], color="green")
    )

    return (
        t + bis + perpediculars + 
        circ + inCenter + 
        outcirc + outCenter
    )

