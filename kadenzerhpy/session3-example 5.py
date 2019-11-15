import rhinoscriptsyntax as rs 
import random

#the goal with this script is to create a surface from any pairs of an A-curve and B-Curve 
#that are closer than a certain threshold

pickedCurves = rs.GetObjects("pick some curves", 4)

if len(pickedCurves) < 2:
	print ("you must pick at least two curves")
else:
	random.shuffle(pickedCurves)
	rs.AddLoftSrf(pickedCurves)



#rs.AddLoftSrf(pickedCurves)






