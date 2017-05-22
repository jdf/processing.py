"""
Code to draw a trefoil knot surface, normals and texture coordinates.
Adapted from the parametric equations example by Philip Rideout:
http://iphone-3d-programming.labs.oreilly.com/ch03.html
"""

def createTrefoil(s, ny, nx, tex):
    """
    This function draws a trefoil knot surface as a triangle mesh derived
    from its parametric equation.
    """

    obj = createShape()
    obj.beginShape(TRIANGLES)
    obj.texture(tex)

    for j in range(nx):
        u0 = float(j) / nx
        u1 = float(j + 1) / nx
        for i in range(ny):
            v0 = float(i) / ny
            v1 = float(i + 1) / ny

            p0 = evalPoint(u0, v0)
            n0 = evalNormal(u0, v0)

            p1 = evalPoint(u0, v1)
            n1 = evalNormal(u0, v1)

            p2 = evalPoint(u1, v1)
            n2 = evalNormal(u1, v1)

            # Triangle p0-p1-p2
            obj.normal(n0.x, n0.y, n0.z)
            obj.vertex(s * p0.x, s * p0.y, s * p0.z, u0, v0)
            obj.normal(n1.x, n1.y, n1.z)
            obj.vertex(s * p1.x, s * p1.y, s * p1.z, u0, v1)
            obj.normal(n2.x, n2.y, n2.z)
            obj.vertex(s * p2.x, s * p2.y, s * p2.z, u1, v1)

            p1 = evalPoint(u1, v0)
            n1 = evalNormal(u1, v0)

            # Triangle p0-p2-p1
            obj.normal(n0.x, n0.y, n0.z)
            obj.vertex(s * p0.x, s * p0.y, s * p0.z, u0, v0)
            obj.normal(n2.x, n2.y, n2.z)
            obj.vertex(s * p2.x, s * p2.y, s * p2.z, u1, v1)
            obj.normal(n1.x, n1.y, n1.z)
            obj.vertex(s * p1.x, s * p1.y, s * p1.z, u1, v0)

    obj.endShape()
    return obj

def evalNormal(u, v):
    """
    Evaluates the surface normal corresponding to normalized parameters (u, v)
    """

    # Compute the tangents and their cross product.
    p = evalPoint(u, v)
    tangU = evalPoint(u + 0.01, v)
    tangV = evalPoint(u, v + 0.01)
    tangU.sub(p)
    tangV.sub(p)

    normUV = tangV.cross(tangU)
    normUV.normalize()
    return normUV


def evalPoint(u, v):
    """
    Evaluates the surface point corresponding to normalized parameters (u, v)
    """

    a, b, c, d = 0.5, 0.3, 0.5, 0.1
    s = TWO_PI * u
    t = (TWO_PI * (1 - v)) * 2

    r = a + b * cos(1.5 * t)
    x = r * cos(t)
    y = r * sin(t)
    z = c * sin(1.5 * t)

    dv = PVector()
    dv.x = (-1.5 * b * sin(1.5 * t) * cos(t) -
            (a + b * cos(1.5 * t)) * sin(t))
    dv.y = (-1.5 * b * sin(1.5 * t) * sin(t) +
            (a + b * cos(1.5 * t)) * cos(t))
    dv.z = 1.5 * c * cos(1.5 * t)

    q = dv
    q.normalize()
    qvn = PVector(q.y, -q.x, 0)
    qvn.normalize()
    ww = q.cross(qvn)

    pt = PVector()
    pt.x = x + d * (qvn.x * cos(s) + ww.x * sin(s))
    pt.y = y + d * (qvn.y * cos(s) + ww.y * sin(s))
    pt.z = z + d * ww.z * sin(s)
    return pt
