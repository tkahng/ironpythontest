import rhinoscriptsyntax as rs

obj = rs.GetObject("Select a srf", rs.filter.surface)
# obj = rs.GetObject("Select object", rs.filter.surface + rs.filter.polysurface)

intervalx = rs.GetReal("intervalx", 1)
intervaly = rs.GetReal("intervaly", 2)
Secx = rs.GetReal("mullion width", 0.15) 
Secy = rs.GetReal("mullion depth", 0.05) 
# domainU = rs.SurfaceDomain(obj, 0)
# domainV = rs.SurfaceDomain(obj, 1)

vec1 = (-Secx/2, -Secy, 0)
vec2 = (-Secx/2, -Secy/2, 0)

def profile(plane, vec):
    rect = rs.AddRectangle( plane, Secx, Secy )
    # rect = rs.MoveObjects(rect, vec)  
    xform = rs.XformTranslation(vec)
    cob = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
    cob_inverse = rs.XformChangeBasis(plane, rs.WorldXYPlane())
    temp = rs.XformMultiply(xform, cob)
    xform2 = rs.XformMultiply(cob_inverse, temp)

    rect = rs.TransformObjects( rect, xform2, True )
    return rect

def sweepSec(crv, plane, vec):
    # plane = rs.CurvePerpFrame(crv, 0)
    # plane = rs.PlaneFromNormal(origin, normal)
    # plane = rs.CurveFrame(crv, 0)
    rs.AddPlaneSurface( plane, 1, 1 )
    rect = profile(plane, vec)
    sweep = rs.AddSweep1(crv, rect, closed=True)
    sweep = rs.CapPlanarHoles(sweep)
    if rect: rs.DeleteObjects(rect)
    if crv: rs.DeleteObjects(crv)
    return sweep

def flipBool(tf):
    return abs(tf-1)

def intervals(uv, spacing):
    domains = []
    domain = rs.SurfaceDomain(obj, uv)
    i = spacing
    while i < domain[1]:
        domains.append(i)
        i = i+spacing
    return domains

def intervalpts(uv, spacing):

    spacings = intervals(uv, spacing)
    ptlist = []

    for i in spacings:
        coord = []
        coord.append(i)
        coord.insert(flipBool(uv), 0)
        ptlist.append(coord)   

    return ptlist

def isoframe(srf, uv, spacing):

    points = intervalpts(uv, spacing)
    print points
    sweeps = []
    
    for i in points:
        point = rs.EvaluateSurface(srf, i[0], i[1])
        parameter = rs.SurfaceClosestPoint(srf, point)
        plane = rs.SurfaceFrame(srf, parameter)
        # plane = rs.PlaneFromFrame( plane.Origin, plane.XAxis, plane.ZAxis)
        crv = rs.ExtractIsoCurve( srf, parameter, flipBool(uv))
        direction = rs.CurveTangent(crv, 0)
        # xaxis = rs.VectorCrossProduct(direction, plane.ZAxis)
        newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
        sweeps.append(sweepSec(crv, newplane, vec2))

    return sweeps    

def extframe(srf):

    crv = rs.DuplicateSurfaceBorder(srf, type=1)
    point = rs.EvaluateCurve(crv, 0)
    parameter = rs.SurfaceClosestPoint(srf, point)
    plane = rs.SurfaceFrame(srf, parameter)
    direction = rs.CurveTangent(crv, 0)
    newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
    frame = sweepSec(crv, newplane, vec1)

    return frame

intframes1 = isoframe(obj, 0, intervalx)
intframes2 = isoframe(obj, 1, intervaly)
extframes = extframe(obj)