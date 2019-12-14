import rhinoscriptsyntax as rs

obj = rs.GetObject("Select a srf", rs.filter.surface)
# obj = rs.GetObject("Select object", rs.filter.surface + rs.filter.polysurface)

intervalx = rs.GetReal("intervalx", 1)
intervaly = rs.GetReal("intervaly", 2.4)
Secx = rs.GetReal("mullion width", 0.15) 
Secy = rs.GetReal("mullion depth", 0.05) 
domainU = rs.SurfaceDomain(obj, 0)
domainV = rs.SurfaceDomain(obj, 1)

vec1 = (-Secx/2, 0, 0)
vec2 = (-Secx/2, -Secx/2, 0)

def profile(plane, vec):
    rect = rs.AddRectangle( plane, Secx, Secy )
    rect = rs.MoveObjects(rect, vec)  
    return rect

def sweepSec(crv, vec):
    plane = rs.CurvePerpFrame(crv, 0)
    rect = profile(plane, vec)
    sweep = rs.AddSweep1(crv,rect, closed=True)
    sweep = rs.CapPlanarHoles(sweep)
    if rect: rs.DeleteObjects(rect)
    if crv: rs.DeleteObjects(crv)
    return sweep

def intframe(domain, srf, interval):
    i = interval   
    sweeps = []
    while i < domain[1]:
        point = rs.EvaluateSurface(srf, i, 0)
        parameter = rs.SurfaceClosestPoint(srf, point)
        crv = rs.ExtractIsoCurve( srf, parameter, 1)
        sweeps.append(sweepSec(crv, vec2))
        i = i+interval  
    return sweeps

def intframe2(domain, srf, interval):
    i = interval   
    sweeps = []
    while i < domain[1]:
        point = rs.EvaluateSurface(srf, 0, i)
        parameter = rs.SurfaceClosestPoint(srf, point)
        crv = rs.ExtractIsoCurve( srf, parameter, 0)
        sweeps.append(sweepSec(crv, vec2))
        i = i+interval  
    return sweeps

def extframe(srf):
    bndry = rs.DuplicateSurfaceBorder(srf, type=1)
    frame = sweepSec(bndry, vec1)
    return frame

intframes1 = intframe(domainU, obj, intervalx)
intframes2 = intframe2(domainV, obj, intervaly)
extframes = extframe(obj)