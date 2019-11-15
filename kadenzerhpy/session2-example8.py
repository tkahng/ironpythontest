import rhinoscriptsyntax as rs 
import random

def randoCurve(nPoints):
	listOfPoints = []
	for q in range(nPoints):
		v1 = random.uniform(-100,100)
		v2 = random.uniform(-100,100)
		v3 = random.uniform(-100,100)
		listOfPoints.append([v1,v2,v3])
	rs.AddInterpCurve(listOfPoints, 3)


#randoCurve(10)
#randoCurve(1000)



for c in range(10):
	randoCurve(c+2)

