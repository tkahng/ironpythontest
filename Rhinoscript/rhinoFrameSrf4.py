import rhinoscriptsyntax as rs

obj = rs.GetObject("Select a srf", rs.filter.surface)
# obj = rs.GetObject("Select object", rs.filter.surface + rs.filter.polysurface)

interval = rs.GetReal("interval", 1)
Secx = rs.GetReal("mullion width", 0.15) 
Secy = rs.GetReal("mullion depth", 0.05) 
domainU = rs.SurfaceDomain(obj, 0)
domainV = rs.SurfaceDomain(obj, 1)

sweeps = []

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

bndry = rs.DuplicateSurfaceBorder(obj, type=1)
frame = sweepSec(bndry, vec1)

i = interval   

while i < domainU[1]:
    point = rs.EvaluateSurface(obj, i, 0)
    parameter = rs.SurfaceClosestPoint(obj, point)
    crv = rs.ExtractIsoCurve( obj, parameter, 1)
    sweeps.append(sweepSec(crv, vec2))
    i = i+interval  


