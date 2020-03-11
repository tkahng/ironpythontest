import rhinoscriptsyntax as rs

iterationCount = 2

obj = rs.GetObject("Select a polyline")

if rs.IsPolyline(obj):
    controlPoints = rs.PolylineVertices(obj)

# if points:
#     for point in points: rs.AddPoint(point)

for j in range(iterationCount):
    newControlPoints = []
    
    for i in range(len(controlPoints)-1):
        oneQuarterPoint = rs.PointAdd(rs.PointScale(controlPoints[i], 0.75),rs.PointScale(controlPoints[i+1], 0.25))   
        newControlPoints.append(rs.CreatePoint(oneQuarterPoint))
        
        threeQuarterPoint = rs.PointAdd(rs.PointScale(controlPoints[i], 0.25),rs.PointScale(controlPoints[i+1], 0.75))
        newControlPoints.append(rs.CreatePoint(threeQuarterPoint))
    
    controlPoints = newControlPoints

rs.AddPolyline(controlPoints)