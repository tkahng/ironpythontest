# !-RunPythonScript "framesrf.py"
# Surface must be Reparametrized with Auto option
import rhinoscriptsyntax as rs
import trkRhinoPy as trp

obj = rs.GetObjects("Select a srf", rs.filter.surface, preselect=True)
eq = rs.GetString('eq?')
eq = not trp.boolToggle(eq)

option = rs.GetInteger('option', number=3)

if option == 2:
    intervalx = rs.GetReal("intervalx", 2)
else:
    intervalx = rs.GetReal("intervalx", 2)
    intervaly = rs.GetReal("intervaly", 2.5)
Secx = rs.GetReal("mullion width", 0.15) 
Secy = rs.GetReal("mullion depth", 0.05) 

vec1 = (-Secx/2, -Secy, 0)
vec2 = (-Secx/2, -Secy/2, 0)

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

def intFlipBool(tf):
    return abs(tf-1)

def Intervals(srf, uv, spacing, eq):
    domains = []
    domain = rs.SurfaceDomain(srf, uv)
    if eq:
        count = int(round(domain[1]/spacing))
        dist = domain[1]/count
    else:
        dist = spacing
    i = dist
    while i < domain[1]:
        domains.append(i)
        i = i+dist
    return domains

def seqIntervals(srf, uv, spacing):
    domains = []
    domain = rs.SurfaceDomain(srf, uv)
    i = spacing
    while i < domain[1]:
        domains.append(i)
        i = i+spacing
    return domains

def intervalpts(srf, uv, spacing):
    spacings = Intervals(srf, uv, spacing, eq)
    ptlist = []
    for i in spacings:
        coord = []
        coord.append(i)
        coord.insert(intFlipBool(uv), 0)
        ptlist.append(coord)   
    return ptlist

def isoframe(srf, uv, spacing, vec):
    points = intervalpts(srf, uv, spacing)
    sweeps = []
    for i in points:
        point = rs.EvaluateSurface(srf, i[0], i[1])
        parameter = rs.SurfaceClosestPoint(srf, point)
        plane = rs.SurfaceFrame(srf, parameter)
        crv = rs.ExtractIsoCurve(srf, parameter, intFlipBool(uv))
        direction = rs.CurveTangent(crv, 0)
        newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
        sweeps.append(sweepSec(crv, newplane, vec))
    print sweeps
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
    print frame
    return frame

def framemulti(srfs):
    rs.EnableRedraw(False)
    if obj:
        rs.SelectObjects(obj)
        rs.Command("reparameterize a")
    frames = []
    for srf in srfs:
        group = rs.AddGroup()
        frame = []
        if option == 2: 
            frame.append(isoframe(srf, 0, intervalx, vec2))
        elif option == 1:
            frame.append(isoframe(srf, 0, intervalx, vec2))
            frame.append(extframe(srf))
        else:
            frame.append(isoframe(srf, 0, intervalx, vec2))
            frame.append(isoframe(srf, 1, intervaly, vec2))
            frame.append(extframe(srf))
        # for f in frame:
        #     print f[0]
        # frame = [frame.append(x) for part in frame for x in part]
        # print rs.AddObjectsToGroup(frame, group)
        # print len(frame)
        # frames.extend(frame)
    # rs.SelectObjects(frames)
    rs.EnableRedraw(True)
    return frames
    
if __name__ == '__main__':
    framemulti(obj)