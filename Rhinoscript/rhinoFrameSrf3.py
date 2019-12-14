import rhinoscriptsyntax as rs

obj = rs.GetObject("Select a srf", rs.filter.surface)
# obj = rs.GetObject("Select object", rs.filter.surface + rs.filter.polysurface)

interval = rs.GetReal("interval", 1)
Secx = rs.GetReal("mullion width", 0.05) 
Secy = rs.GetReal("mullion depth", 0.05) 
domainU = rs.SurfaceDomain(obj, 0)
domainV = rs.SurfaceDomain(obj, 1)

rails = []
shapes = []
sweeps = []

def profile1(plane):
    planept = rs.EvaluatePlane(plane, (0,0))
    rect = rs.AddRectangle( plane, Secx, Secy )
    cen = rs.CurveAreaCentroid(rect)
    vec = planept - cen[0]
    rect = rs.MoveObjects(rect, vec)  
    sweep = rs.AddSweep1(crv,rect)
    if rect: rs.DeleteObjects(rect)
    # if crv: rs.DeleteObjects(crv)
    return sweep

def profile2(plane):
    planept = rs.EvaluatePlane(plane, (0,0))
    rect = rs.AddRectangle( plane, Secx, Secy )
    cen = rs.CurveAreaCentroid(rect)
    vec = (Secx/2, 0, 0)
    rect = rs.MoveObjects(rect, vec)  
    sweep = rs.AddSweep1(crv,rect)
    if rect: rs.DeleteObjects(rect)
    # if crv: rs.DeleteObjects(crv)
    return sweep

def sweepSec(crv):
    plane = rs.CurvePerpFrame(crv, 0)
    planept = rs.EvaluatePlane(plane, (0,0))
    rect = rs.AddRectangle( plane, Secx, Secy )
    cen = rs.CurveAreaCentroid(rect)
    vec = planept - cen[0]
    rect = rs.MoveObjects(rect, vec)  
    sweep = rs.AddSweep1(crv,rect)
    if rect: rs.DeleteObjects(rect)
    # if crv: rs.DeleteObjects(crv)
    return sweep

def sweepSec2(crv):
    plane = rs.CurvePerpFrame(crv, 0)
    planept = rs.EvaluatePlane(plane, (0,0))
    rect = rs.AddRectangle( plane, Secx, Secy )
    cen = rs.CurveAreaCentroid(rect)
    vec = (-Secx/2, 0, 0)
    rect = rs.MoveObjects(rect, vec)  
    sweep = rs.AddSweep1(crv,rect)
    if rect: rs.DeleteObjects(rect)
    # if crv: rs.DeleteObjects(crv)
    return sweep

def sweepSec3(crv):
    plane = rs.CurvePerpFrame(crv, 0)
    planept = rs.EvaluatePlane(plane, (0,0))
    rect = rs.AddRectangle( plane, Secx, Secy )
    cen = rs.CurveAreaCentroid(rect)
    vec = planept - cen[0]
    rect = rs.MoveObjects(rect, vec)  
    sweep = rs.AddSweep1(crv,rect)
    if rect: rs.DeleteObjects(rect)
    # if crv: rs.DeleteObjects(crv)
    return sweep

bndry = rs.DuplicateSurfaceBorder(obj, type=1)
frame = sweepSec2(bndry)

i = interval   

while i < domainU[1]:
    point = rs.EvaluateSurface(obj, i, 0)
    parameter = rs.SurfaceClosestPoint(obj, point)
    crv = rs.ExtractIsoCurve( obj, parameter, 1)
    sweeps.append(sweepSec(crv))

    if crv: rs.DeleteObjects(crv)
    i = i+interval  

if rails: rs.DeleteObjects(rails)
if shapes: rs.DeleteObjects(shapes)


