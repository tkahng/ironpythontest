import rhinoscriptsyntax as rs


curves = rs.ObjectsByType(4)
picturePlane = rs.GetObject("select the surface to use as the picture plane", 8)
eyePoint = rs.GetObject("select the point to use as the eye, the point at which the projected content will converge",1)

#note that we wouldn't need an eye point if our projectors are paralell

for curve in curves:
	pointsOnCurve = rs.DivideCurve(curve, 100)
	intersectionPoints = []
	for point in pointsOnCurve:
		projector = rs.AddLine(point, eyePoint)
		intersections = rs.CurveSurfaceIntersection(projector, picturePlane)
		if intersections:
			intersectionPoint = intersections[0][1]
			intersectionPoints.append(intersectionPoint)
	rs.AddPoints(intersectionPoints)
	rs.AddInterpCurve(intersectionPoints, 1) #what would be a more precise way to reconstruct the curve?

#add layer management to sep process content from finish content, and to use close/far distinction
