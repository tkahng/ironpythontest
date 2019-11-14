    # for (int j = 0; j < iterationCount; j++)
    # {
    #   List<Point3d> newControlPoints = new List<Point3d>();

    #   for (int i = 0; i < controlPoints.Count - 1; i++)
    #   {
    #     Point3d oneQuarterPoint = 0.75 * controlPoints[i] + 0.25 * controlPoints[i + 1];
    #     newControlPoints.Add(oneQuarterPoint);

    #     Point3d threeQuarterPoint = 0.25 * controlPoints[i] + 0.75 * controlPoints[i + 1];
    #     newControlPoints.Add(threeQuarterPoint);
    #   }

    #   controlPoints = newControlPoints;
    # }

    # curve = new PolylineCurve(controlPoints);


import rhinoscriptsyntax as rs

for j in range(iterationCount):
    newControlPoints = []
    
    for i in range(len(controlPoints)-1):
        oneQuarterPoint = rs.PointAdd(rs.PointScale(controlPoints[i], 0.75),rs.PointScale(controlPoints[i+1], 0.25))   
        newControlPoints.append(rs.CreatePoint(oneQuarterPoint))
        
        threeQuarterPoint = rs.PointAdd(rs.PointScale(controlPoints[i], 0.25),rs.PointScale(controlPoints[i+1], 0.75))
        newControlPoints.append(rs.CreatePoint(threeQuarterPoint))
    
    controlPoints = newControlPoints

curve = rs.AddPolyline(controlPoints)