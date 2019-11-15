import rhinoscriptsyntax as rs 
import random

#the goal with this script is to create a surface from any pairs of an A-curve and B-Curve 
#that are closer than a certain threshold

pickedCurvesA = rs.GetObjects("pick some curves for set A", 4)

pickedCurvesB = rs.GetObjects("pick some curves for set B", 4)

threshold = rs.GetReal("set distance threshold")




for aCurve in pickedCurvesA:
	for bCurve in pickedCurvesB:
		pointOnA = rs.CurveMidPoint(aCurve)
		pointOnB = rs.CurveMidPoint(bCurve)
		if rs.Distance (pointOnA, pointOnB) < threshold:
			rs.AddLoftSrf([aCurve, bCurve])
		
