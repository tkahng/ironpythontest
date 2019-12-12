import rhinoscriptsyntax as rs

# obj = rs.GetObject("Select a srf", rs.filter.surface)

obj = rs.GetObject("Select object", rs.filter.surface + rs.filter.polysurface)
# startpoint = rs.GetPoint("Base point of center line")
# endpoint = rs.GetPoint("Endpoint of center line", startpoint)
# contours = rs.AddSrfContourCrvs( obj, (startpoint, endpoint) )

interval = rs.GetReal("interval", 1.0)

# if rs.IsSurface(obj):
#     sd

domainU = rs.SurfaceDomain(obj, 0)
domainV = rs.SurfaceDomain(obj, 1)

evalpt = []

while i < domainU:
    pt = i+interval
    

point = rs.GetPointOnSurface(obj, "Select location for extraction")
parameter = rs.SurfaceClosestPoint(obj, point)
rs.ExtractIsoCurve( obj, parameter, 2 )

object_ids = rs.GetObjects("Select objects to delete")
if object_ids: rs.DeleteObjects(object_ids)




import rhinoscriptsyntax as rs
plane = rs.WorldXYPlane()
plane = rs.RotatePlane(plane, 45.0, [0,0,1])
planept = rs.EvaluatePlane(plane, (0,0))
rect = rs.AddRectangle( plane, 5.0, 15.0 )
cen = rs.CurveAreaCentroid(rect)
vec = planept - cen[0]
rs.MoveObjects(rect, vec)
