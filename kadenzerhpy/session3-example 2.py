import rhinoscriptsyntax as rs 
import random

pickedCurves = rs.GetObjects("pick some curves", 4)

for curve in pickedCurves:
	#note, this is a good example of crafring procedure in reverse
	startPoint = rs.CurveMidPoint(curve)
	
	goalPoint = (startPoint[0], startPoint[1], 0)
	
	pathLine = rs.AddLine(startPoint, goalPoint)
	



	rs.ExtrudeCurve(curve, pathLine)
	rs.DeleteObject(pathLine)
	
