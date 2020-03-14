# !-RunPythonScript "framesrf.py"
# Surface must be Reparametrized with Auto option
import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects("Select a srf", rs.filter.surface, preselect=True)

# intervalx = rs.GetReal("intervalx", 1)
# intervaly = rs.GetReal("intervaly", 2)
# Secx = rs.GetReal("mullion width", 0.15) 
# Secy = rs.GetReal("mullion depth", 0.05) 
Secx = 0.15 
Secy = 0.05 
vec1 = (-Secx/2, -Secy, 0)
vec2 = (-Secx/2, -Secy/2, 0)

rs.EnableRedraw(False)

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
    # sweep = rs.CapPlanarHoles(sweep)
    rs.CapPlanarHoles(sweep)
    if rect: rs.DeleteObjects(rect)
    if crv: rs.DeleteObjects(crv)
    return sweep[0]

def setDist(length, dist, eq):
    if eq:
        count = int(length/dist)
        dist = length/count
    return dist

def sweepRail(srf, crv, vec, param, point):
    plane = rs.SurfaceFrame(srf, param)
    direction = rs.CurveTangent(crv, 0)
    newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
    # if crv: rs.DeleteObjects(crv)
    return sweepSec(crv, newplane, vec)

def getDiv(srf, dist, uv, eq):
    domaincrv = rs.ExtractIsoCurve( srf, [0,0], uv)
    crvLen = rs.CurveLength(domaincrv)
    newdist = setDist(crvLen, dist, eq)
    pts = rs.DivideCurveLength(domaincrv, newdist)
    pts.pop(0)
    pts.pop(-1)
    rs.DeleteObject(domaincrv)
    return pts

def getEnds(srf, uv):
    domaincrv = rs.ExtractIsoCurve( srf, [0,0], uv)
    return [rs.CurveStartPoint(domaincrv), rs.CurveEndPoint(domaincrv)]
    rs.DeleteObject(domaincrv)

def divCrv(srf, pts, uv, vec, eq):
    param = map(lambda x: rs.SurfaceClosestPoint(srf, x), pts)
    railcrv = map(lambda x: rs.ExtractIsoCurve( srf, x, trp.intFlipBool(uv)), param)
    frames = map(lambda x, y, z: sweepRail(srf, x, vec, y, z), railcrv, param, pts)
    # rs.DeleteObject(domaincrv)
    return railcrv


def makeFrame(srf, dist, uv, vec, eq):
    pts = getDiv(srf, dist, uv, eq)
    # points = getEnds(srf, uv)
    divCrv(srf, pts, uv, vec, eq)

def makeExt(srf, dist, uv, vec, eq):
    # points = getDiv(srf, dist, uv, eq)
    pts = getEnds(srf, uv)
    divCrv(srf, pts, uv, vec, eq)

map(lambda x: makeFrame(x, 3, 1, vec2, True), objs)
map(lambda x: makeFrame(x, 3, 0, vec2, True), objs)
map(lambda x: makeExt(x, 3, 1, vec1, True), objs)
map(lambda x: makeExt(x, 3, 0, vec1, True), objs)

rs.EnableRedraw(True)

# def divCrv(srf, dist, uv, eq):
#     domaincrv = rs.ExtractIsoCurve( srf, [0,0], uv)
#     crvLen = rs.CurveLength(domaincrv)
#     newdist = setDist(crvLen, dist, eq)
#     # pts = rs.DivideCurveEquidistant(domaincrv, dist)
#     pts = rs.DivideCurveLength(domaincrv, newdist)
#     # pts.append(rs.CurveEndPoint(domaincrv))
#     # print pts[0]
#     param = map(lambda x: rs.SurfaceClosestPoint(srf, x), pts)
#     railcrv = map(lambda x: rs.ExtractIsoCurve( srf, x, trp.intFlipBool(uv)), param)
#     frames = map(lambda x, y, z: sweepRail(srf, x, vec2, y, z), railcrv, param, pts)
#     # rs.DeleteObject(domaincrv)
#     return railcrv

# def divCrv(srf, dist, uv, eq):
#     domaincrv = rs.ExtractIsoCurve( srf, [0,0], uv)
#     crvLen = rs.CurveLength(domaincrv)
#     newdist = setDist(crvLen, dist, eq)

#     pts = rs.DivideCurveLength(domaincrv, newdist)

#     param = map(lambda x: rs.SurfaceClosestPoint(srf, x), pts)
#     railcrv = map(lambda x: rs.ExtractIsoCurve( srf, x, trp.intFlipBool(uv)), param)
#     frames = map(lambda x, y, z: sweepRail(srf, x, vec2, y, z), railcrv, param, pts)
#     # rs.DeleteObject(domaincrv)
#     return railcrv