import rhinoscriptsyntax as rs 
import random, math

def blipCurve(y):
	listOfPoints=[]
	for x in range(0,750,20):
		z = (x/5)*math.sin(x/50)+20*math.sin(x+y/20)
		if x == 640:
			z+=random.uniform(-30,30)
			x+=random.uniform(-30,30)
		listOfPoints.append((x,y,z))

	return rs.AddInterpCurve(listOfPoints,3)

def veryBlipCurve(y):
	listOfPoints=[]
	for x in range(0,750,20):
		z = (x/5)*math.sin(x/50)+20*math.sin(x+y/20)
		
		z+=random.uniform(-5,5)
		x+=random.uniform(-5,5)
		listOfPoints.append((x,y,z))

	return rs.AddInterpCurve(listOfPoints,3)


for c in range(0,3000,3):
	aCurve = blipCurve(c)
	if c == 300:
		veryBlipCurve(c)
	else:
		blipCurve(c)