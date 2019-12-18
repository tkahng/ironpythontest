import rhinoscriptsyntax as rs
objs = rs.GetObjects("Pick curves to loft", rs.filter.curve)
width = rs.GetReal("width", 0.4)
plane = rs.ViewCPlane()
# if objs: rs.AddLoftSrf(objs)
# curve = rs.AddLine((5,0,0), (10,0,10))
# surface = rs.AddSrfPt([(0,0,0), (5,0,0), (5,5,0), (0,5,0)])
# rs.ExtrudeSurface(surface, curve)
# def flatten(l):
#     for el in l:
#         if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
#             for sub in flatten(el):
#                 yield sub
#         else:
#             yield el

def offsetBothCrvs(crvs, width):
    loftCrvs = []
    if rs.IsCurve(crvs): 
        loftCrvs.append(rs.OffsetCurve( crvs, [0,0,0], width/2))
        loftCrvs.append(rs.OffsetCurve( crvs, [0,0,0], -width/2))
    return rs.AddLoftSrf(loftCrvs)
    # if loftCrvs: rs.DeleteObjects(reloftCrvs)

# def returnSelection():
#     objs = rs.LastCreatedObjects()
#     if objs:
#         # Only the last circle will be selected
#         rs.SelectObjects(objs)

def addRail(obj):
    vec = rs.CreateVector(0, 0, 4)
    point1 = rs.EvaluateCurve(obj, 0)
    point2 = rs.MoveObject(obj, vec)
    return rs.AddLine(point1, point2)

def makeWall(crvs, width):
    # if crvs:
    breps = []
    for crv in crvs:
        inputsrf = offsetBothCrvs(crv, width)
        railCurve = addRail(crv)
        brep = rs.ExtrudeSurface(surface, curve)
        breps.append(brep)
    return breps

makeWall(objs, width)


        
