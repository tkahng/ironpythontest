import rhinoscriptsyntax as rs 
import random

#the goal with this script is to create a surface from any pairs of an A-curve and B-Curve 
#that are closer than a certain threshold

pickedCurves = rs.GetObjects("pick some curves", 4)

pickedPoints = rs.GetObjects("pick some point objects", 1)


for curve in pickedCurves:
	
	distances=[]
	for point in pickedPoints:
		#note here about choices when coding-- how much to compress multiple functions to one line
		#efficiency vs. clarity
		thisDistance = rs.Distance(point, rs.CurveMidPoint(curve))
		distances.append(thisDistance)
	



	distancesAndPointsPaired = zip(distances, pickedPoints)
	#print distancesAndPointsPaired
	
	distancesAndPointsPaired.sort()

	closestPoint = distancesAndPointsPaired[0][1]
	rs.ExtrudeCurvePoint(curve, closestPoint)

	#what if we wanted to get the farthest point?



