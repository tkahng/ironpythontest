import rhinoscriptsyntax as rs

obj = rs.GetObjects("Select a srf", rs.filter.surface)

intervalx = rs.GetReal("intervalx", 1)
intervaly = rs.GetReal("intervaly", 2)
Secx = rs.GetReal("mullion width", 0.15) 
Secy = rs.GetReal("mullion depth", 0.05) 
louverW = rs.GetReal("louverW width", 0.5) 

vec1 = (-Secx/2, -Secy, 0)
vec2 = (-Secx/2, -Secy/2, 0)
vec3 = (-louverW/2, -louverW/2, 0)

def rectFrame():
    return rs.AddRectangle(rs.WorldXYPlane(), Secx, Secy )

def profileXform(sec, plane, vec):
    xvec = rs.XformTranslation(vec)
    cob = rs.XformChangeBasis(plane, rs.WorldXYPlane())
    xform = rs.XformMultiply(cob, xvec)
    return rs.TransformObjects(sec, xform, False)

def sweepSec(crv, plane, vec):
    rect = profileXform(rectFrame(), plane, vec)
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

def isoframe(srf, uv, spacing, vec):
    points = intervalpts(srf, uv, spacing)
    # print points
    sweeps = []
    for i in points:
        point = rs.EvaluateSurface(srf, i[0], i[1])
        parameter = rs.SurfaceClosestPoint(srf, point)
        plane = rs.SurfaceFrame(srf, parameter)
        crv = rs.ExtractIsoCurve( srf, parameter, flipBool(uv))
        direction = rs.CurveTangent(crv, 0)
        newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
        sweeps.append(sweepSec(crv, newplane, vec))
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

def framelouver(srf):
    frames = []
    frames.append(isoframe(srf, 0, intervalx, vec3))
    return frames
    
def frameall(srf):
    frames = []
    framesv = isoframe(srf, 0, intervalx, vec2)
    framesh = isoframe(srf, 1, intervaly, vec2)
    frameso = extframe(srf)

    frames.append(rs.BooleanDifference(framesh, framesv))

    return frames

def framemulti(srfs):
    frames = []
    for srf in srfs:
        frames.append(frameall(srf))
        # frames.append(isoframe(srf, 0, intervalx, vec2))
        # frames.append(isoframe(srf, 1, intervaly, vec2))
        # frames.append(extframe(srf))
    return frames
    
if __name__ == '__main__':
    framemulti(obj)

