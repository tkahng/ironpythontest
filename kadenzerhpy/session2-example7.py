import rhinoscriptsyntax as rs 
import random


for c in range(3):
	listOfPoints = []
	for q in range(50):
		v1 = random.uniform(-100,100)
		v2 = random.uniform(-100,100)
		v3 = random.uniform(-100,100)
		listOfPoints.append([v1,v2,v3])
	rs.AddInterpCurve(listOfPoints, 3)

