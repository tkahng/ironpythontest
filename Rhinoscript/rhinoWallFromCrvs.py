import rhinoscriptsyntax as rs
objs = rs.GetObjects("Pick curves to loft", rs.filter.curve)
width = rs.GetReal("width", 0.4)
plane = rs.ViewCPlane()
# if objs: rs.AddLoftSrf(objs)
# curve = rs.AddLine((5,0,0), (10,0,10))
# surface = rs.AddSrfPt([(0,0,0), (5,0,0), (5,5,0), (0,5,0)])
# rs.ExtrudeSurface(surface, curve)

def offsetBothCrvs(crvs, width):
    offsets = [] 
    offsets.append(rs.OffsetCurve( crvs, [0,0,0], width/2))
    offsets.append(rs.OffsetCurve( crvs, [0,0,0], -width/2))
    section = rs.AddLoftSrf(offsets,loft_type=2)
    return section

# def returnSelection():
#     objs = rs.LastCreatedObjects()
#     if objs:
#         # Only the last circle will be selected
#         rs.SelectObjects(objs)

def addRail(obj):
    point1 = rs.EvaluateSurface(obj, 0, 0)
    vec = rs.CreateVector(0, 0, 4)
    point2 = rs.CopyObject(point1, vec)
    return rs.AddLine(point1, point2)

def makeWall(crvs, width):
    breps = []
    shapes = []

    for crv in crvs:
        shape = offsetBothCrvs(crv, width)
        if rs.IsPolysurface(shape):
            surfs =rs.ExplodePolysurfaces(shape)
            for surf in surfs:
                shapes.append(surf)
        else:
            shapes.append(shape)

    for shape in shapes:
        railCurve = addRail(shape)
        breps.append(rs.ExtrudeSurface(shape, railCurve))
        
    return breps

makeWall(objs, width)


        
