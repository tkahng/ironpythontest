import rhinoscriptsyntax as rs

obj = rs.GetObject("Select a srf", rs.filter.surface)

# obj = rs.GetObject("Select object", rs.filter.surface + rs.filter.polysurface)

interval = rs.GetReal("interval", 1)

domainU = rs.SurfaceDomain(obj, 0)
domainV = rs.SurfaceDomain(obj, 1)

# interval = 1.2
# domainU = 3.2
rails = []
shapes = []

i = 0   

while i < domainU[1]:
    point = rs.EvaluateSurface(obj, i, 0)
    # rs.AddPoint(point)
    parameter = rs.SurfaceClosestPoint(obj, point)
    # rails.append(rs.ExtractIsoCurve( obj, parameter, 1))
    # crv = rails
    
    crv = rs.ExtractIsoCurve( obj, parameter, 1)


    rails.append(crv)

    plane = rs.CurvePerpFrame(crv, 0)
    planept = rs.EvaluatePlane(plane, (0,0))
    rect = rs.AddRectangle( plane, 0.1, 0.1 )
    cen = rs.CurveAreaCentroid(rect)
    vec = planept - cen[0]
    # rs.MoveObjects(rect, vec)
    # rs.AddSweep1(crv,rect)

    shapes.append(rs.MoveObjects(rect, vec))

    i = i+interval  

print rails
print shapes

for j in range(len(rails)):
    rs.AddSweep1(rails[j],shapes[j])

# for rail in rails:
#     # rail = rails[i]
#     plane = rs.CurvePerpFrame(rail, 0)
#     planept = rs.EvaluatePlane(plane, (0,0))
#     rect = rs.AddRectangle( plane, 0.1, 0.1 )
#     cen = rs.CurveAreaCentroid(rect)
#     vec = planept - cen[0]
#     rs.MoveObjects(rect, vec)
#     rs.AddSweep1(rail,rect)




# object_ids = rs.GetObjects("Select objects to delete")
# if object_ids: rs.DeleteObjects(object_ids)


