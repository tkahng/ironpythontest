import rhinoscriptsyntax as rs

# obj = rs.GetObject("Select a srf", rs.filter.surface)

obj = rs.GetObject("Select object", rs.filter.surface + rs.filter.polysurface)


interval = rs.GetReal("interval", 1.0)

# if rs.IsSurface(obj):
#     sd

domainU = rs.SurfaceDomain(obj, 0)
domainV = rs.SurfaceDomain(obj, 1)

# interval = 1.2
# domainU = 3.2
evalpt = []

i = 0

while i < domainU:
    point = rs.EvaluateSurface(obj, interval, 1)
    rs.AddPoint(point)
    # evalpt.append(i)
    i = i+interval

# print(evalpt)
    

# point = rs.GetPointOnSurface(obj, "Select location for extraction")
# parameter = rs.SurfaceClosestPoint(obj, point)
# rs.ExtractIsoCurve( obj, parameter, 2 )

# object_ids = rs.GetObjects("Select objects to delete")
# if object_ids: rs.DeleteObjects(object_ids)




# import rhinoscriptsyntax as rs
# plane = rs.WorldXYPlane()
# plane = rs.RotatePlane(plane, 45.0, [0,0,1])
# planept = rs.EvaluatePlane(plane, (0,0))
# rect = rs.AddRectangle( plane, 5.0, 15.0 )
# cen = rs.CurveAreaCentroid(rect)
# vec = planept - cen[0]
# rs.MoveObjects(rect, vec)
