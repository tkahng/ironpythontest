import rhinoscriptsyntax as rs
objs = rs.GetObjects("Pick curves to loft", rs.filter.curve)
width = rs.GetReal("width", 0.4)
plane = rs.ViewCPlane()
# if objs: rs.AddLoftSrf(objs)
# curve = rs.AddLine((5,0,0), (10,0,10))
# surface = rs.AddSrfPt([(0,0,0), (5,0,0), (5,5,0), (0,5,0)])
# rs.ExtrudeSurface(surface, curve)

def offsetBothCrvs(crvs, width):
    lofts = []
    loftCrvs = []
    # if rs.IsCurve(crvs):
    offsets = [] 
    offsets.append(rs.OffsetCurve( crvs, [0,0,0], width/2))
    offsets.append(rs.OffsetCurve( crvs, [0,0,0], -width/2))
    # for i in offsets:

        
    section = rs.AddLoftSrf(offsets,loft_type=2)
    if rs.IsPolysurface(section):
        lofts.append(rs.ExplodePolysurfaces(section))
    else:
        lofts.append(section)
    return lofts
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
    point2 = rs.CopyObject(point1, vec)
    return rs.AddLine(point1, point2)


def makeWall(crvs, width):
    # if crvs:
    breps = []
    for crv in crvs:
        railCurve = addRail(crv)
        shape = offsetBothCrvs(crv, width)
        brep = rs.ExtrudeSurface(shape, railCurve)
        breps.append(brep)
    return breps

makeWall(objs, width)


        
