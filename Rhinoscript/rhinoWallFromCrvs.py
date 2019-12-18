import rhinoscriptsyntax as rs

objs = rs.GetObjects("Pick curves to loft", rs.filter.curve)
width = rs.GetReal("width", 0.4)
height = rs.GetReal("height", 3)
plane = rs.ViewCPlane()

def offsetBothCrvs(crvs, width):
    offsets = [] 
    offsets.append(rs.OffsetCurve( crvs, [0,0,0], width/2))
    offsets.append(rs.OffsetCurve( crvs, [0,0,0], -width/2))
    section = rs.AddLoftSrf(offsets,loft_type=2)
    if offsets: rs.DeleteObjects(offsets)
    return section

def addRail(obj):
    point1 = rs.EvaluateSurface(obj, 0, 0)
    vec = rs.CreateVector(0, 0, height)
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


        
