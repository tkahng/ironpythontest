import rhinoscriptsyntax as rs 
import random

pickedCurves = rs.GetObjects("pick some curves", 4)
desiredArea = 1000.0

for curve in pickedCurves:
	length = rs.CurveLength(curve)
	extrudeAmt = desiredArea/length
	direcitonalVector = (random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10))
	#how we have a vector with random x, y and z components
	#to give it the precise amplitude we want, we will normalize it, meaning it will keep the direction, but have a length of one unit
	#then, we'll scale the vector to the desired amplitude

	unitVect = rs.VectorUnitize(direcitonalVector)
	
	scaledVect = rs.VectorScale(unitVect, extrudeAmt)

	startPoint = rs.CurveMidPoint(curve)
	endPoint = rs.VectorAdd(startPoint, scaledVect)
	

	pathCurve = rs.AddLine(startPoint,endPoint)
	

	rs.ExtrudeCurve(curve,pathCurve)
	rs.DeleteObject(pathCurve)
	#further example: how to put the surface on a new layer	
