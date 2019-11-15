import rhinoscriptsyntax as rs


curves = rs.ObjectsByType(4)
picturePlane = rs.GetObject("select the surface to use as the picture plane", 8)
eyePoint = rs.GetObject("select the point to use as the eye, the point at which the projected content will converge",1)

#note that we wouldn't need an eye point if our projectors are paralell

for curve in curves:
	pointsOnCurve = rs.DivideCurve(curve, 100)
	intersectionPoints = []
	closeCount = 0
	middleCount = 0
	farCount = 0
	for point in pointsOnCurve:
		
		if rs.Distance(point, eyePoint) < 1000:
			layerName = "close"
			closeCount+=1
		elif rs.Distance(point, eyePoint) >= 1000 and rs.Distance(point, eyePoint) <1300:
			layerName = "middle"
			middleCount+=1
		else:
			layerName = "far"
			farCount+=1



		projector = rs.AddLine(point, eyePoint)
		
		rs.ObjectLayer(projector, layerName)

		intersections = rs.CurveSurfaceIntersection(projector, picturePlane)
		if intersections:
			intersectionPoint = intersections[0][1]
			pointObjectInSpace = rs.AddPoint(point)
			rs.ObjectLayer(pointObjectInSpace, layerName)
			intersectionPoints.append(intersectionPoint)



	pointObs = rs.AddPoints(intersectionPoints)
	reconstructedCurve = rs.AddInterpCurve(intersectionPoints, 1) #what would be a more precise way to reconstruct the curve?

	if closeCount > middleCount and closeCount > farCount:
		rs.ObjectLayer(reconstructedCurve, "close")

	elif middleCount>farCount:
		rs.ObjectLayer(reconstructedCurve, "middle")

	else:
		rs.ObjectLayer(reconstructedCurve, "far")




#add layer management to sep process content from finish content, and to use close/far distinction
