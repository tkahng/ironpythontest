import rhinoscriptsyntax as rs 
import random


pickedCurves = rs.GetObjects("pick some curves", 4)



for curve in pickedCurves:
	counter = 0
	vector = (random.uniform(-5,5),random.uniform(-5,5),random.uniform(-5,5))
	newCurve = rs.CopyObject(curve, vector)
	surface = rs.AddLoftSrf([curve, newCurve])
	newCurveMidPoint = rs.CurveMidPoint(newCurve)
	x=newCurveMidPoint[0]
	y=newCurveMidPoint[1]
	z=newCurveMidPoint[2]
	while x < 100 and x> -100 and y <100 and y> -100 and z < 100 and z > -100:
		counter+=1
		previousCurve = newCurve
		newCurve = rs.CopyObject(newCurve, vector)
		newCurveMidPoint = rs.CurveMidPoint(newCurve)
		x=newCurveMidPoint[0]
		y=newCurveMidPoint[1]
		z=newCurveMidPoint[2]
		if counter % 2 ==0:
			surface = rs.AddLoftSrf([previousCurve, newCurve])
			


		





