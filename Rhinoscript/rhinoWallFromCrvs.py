import rhinoscriptsyntax as rs
objs = rs.GetObjects("Pick curves to loft", rs.filter.curve)
width = rs.GetReal("width", 0.4)
plane = rs.ViewCPlane()
# if objs: rs.AddLoftSrf(objs)
# curve = rs.AddLine((5,0,0), (10,0,10))
# surface = rs.AddSrfPt([(0,0,0), (5,0,0), (5,5,0), (0,5,0)])
# rs.ExtrudeSurface(surface, curve)

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
    point1 = rs.EvaluateCurve(obj, 0)
    vec = rs.CreateVector(0, 0, 4)
    matrix = rs.XformTranslation(vec)
    point2 = rs.MoveObjects(point1, vec)
    return rs.AddLine(point1, point2)

def makeWall(crvs, width):
    # if crvs:
    breps = []
    for crv in crvs:
        inputsrf = offsetBothCrvs(crv, width)
        railCurve = addRail(crv)
        brep = rs.ExtrudeSurface(inputsrf, crvs)
        breps.append(brep)
    return breps

makeWall(objs, width)


        
