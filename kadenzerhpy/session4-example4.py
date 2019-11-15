# draw lines normal to surface
import rhinoscriptsyntax as rs
import random

def tree(trunk, desiredLevel, vectorDirection, currentlevel=0):

	endPoint = rs.CurveEndPoint(trunk)
	print vectorDirection
	adjustedVector1 = (vectorDirection[0]+random.uniform(-3,3),vectorDirection[1]+random.uniform(-3,3),vectorDirection[2]+random.uniform(0,3))
	adjustedVector2 = (vectorDirection[0]+random.uniform(-3,3),vectorDirection[1]+random.uniform(-3,3),vectorDirection[2]+random.uniform(0,3))

	newPoint1 = (endPoint[0]+adjustedVector1[0],endPoint[1]+adjustedVector1[1],endPoint[2]+adjustedVector1[2])
	newPoint2 = (endPoint[0]+adjustedVector2[0],endPoint[1]+adjustedVector2[1],endPoint[2]+adjustedVector2[2])

	newBranch1 = rs.AddLine(endPoint,newPoint1)
	newBranch2 = rs.AddLine(endPoint,newPoint2)

	if currentlevel<desiredLevel:
		tree(newBranch1,desiredLevel, adjustedVector1, currentlevel+1)
		tree(newBranch2,desiredLevel, adjustedVector2, currentlevel+1)

startLine = rs.AddLine((0,0,0),(4,18,8))
tree(startLine,7, (2,9,4))