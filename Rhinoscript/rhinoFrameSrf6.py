import rhinoscriptsyntax as rs

obj = rs.GetObjects("Select a srf", rs.filter.surface)
# obj = rs.GetObject("Select object", rs.filter.surface + rs.filter.polysurface)

intervalx = rs.GetReal("intervalx", 1)
intervaly = rs.GetReal("intervaly", 2)
Secx = rs.GetReal("mullion width", 0.15) 
Secy = rs.GetReal("mullion depth", 0.05) 

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
    rect2 = rs.TransformObjects( rect, xform2, True )
    if rect: rs.DeleteObjects(rect)
    return rect2

def sweepSec(crv, plane, vec):
    # rs.AddPlaneSurface( plane, 1, 1 )
    rect = profile(plane, vec)
    sweep = rs.AddSweep1(crv, rect, closed=True)
    sweep = rs.CapPlanarHoles(sweep)
    if rect: rs.DeleteObjects(rect)
    if crv: rs.DeleteObjects(crv)
    return sweep

def flipBool(tf):
    return abs(tf-1)

def intervals(srf, uv, spacing):
    domains = []
    domain = rs.SurfaceDomain(srf, uv)
    i = spacing
    while i < domain[1]:
        domains.append(i)
        i = i+spacing
    return domains

def intervalpts(srf, uv, spacing):

    spacings = intervals(srf, uv, spacing)
    ptlist = []
    
    for i in spacings:
        coord = []
        coord.append(i)
        coord.insert(flipBool(uv), 0)
        ptlist.append(coord)   

    return ptlist

def isoframe(srf, uv, spacing):

    points = intervalpts(srf, uv, spacing)
    print points
    sweeps = []
    
    for i in points:
        point = rs.EvaluateSurface(srf, i[0], i[1])
        parameter = rs.SurfaceClosestPoint(srf, point)
        plane = rs.SurfaceFrame(srf, parameter)
        crv = rs.ExtractIsoCurve( srf, parameter, flipBool(uv))
        direction = rs.CurveTangent(crv, 0)
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
    if crv: rs.DeleteObjects(crv)

    return frame

def frameall(srf):
    frames = []
    frames.append(isoframe(srf, 0, intervalx))
    frames.append(isoframe(srf, 1, intervaly))
    frames.append(extframe(srf))
    return frames

def framemulti(srfs):
    frames = []

    for srf in srfs:
        frames.append(frameall(srf))
    
    return frames
    

framemulti(obj)
