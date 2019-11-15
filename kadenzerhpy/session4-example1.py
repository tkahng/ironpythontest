import rhinoscriptsyntax as rs


#this script takes a surface as input and draws a grid on the "local" UV coordinate system of that surface


srf = rs.GetObject("pick surface", 8)



numberUCells= 12
numberVCells= 20

uDomain = rs.SurfaceDomain(srf, 0)
vDomain = rs.SurfaceDomain(srf, 1)


"""
print (uDomain)
print (vDomain)

pointCoordinatesA = rs.EvaluateSurface(srf, 10, 145)
pointCoordinatesB = rs.EvaluateSurface(srf, 20, 145)
pointCoordinatesC = rs.EvaluateSurface(srf, 30, 145)

rs.AddPoint(pointCoordinatesA)
rs.AddPoint(pointCoordinatesB)
rs.AddPoint(pointCoordinatesC)
"""


uMin = uDomain[0]
uMax = uDomain[1]
vMin = vDomain[0]
vMax = vDomain[1]

uRange = uMax-uMin
vRange = vMax-vMin

uStep = uRange/numberUCells
vStep = vRange/numberVCells

U = uMin
while U < uMax:
	V = vMin
	while V<vMax:
		

		pointA = rs.EvaluateSurface(srf, U, V)
		pointB = rs.EvaluateSurface(srf, U+uStep, V)
		pointC = rs.EvaluateSurface(srf, U+uStep, V+vStep)
		pointD = rs.EvaluateSurface(srf, U, V+vStep)
		
		poly= rs.AddPolyline([pointA, pointB, pointC, pointD, pointA])
		
		#would be easy to do all sorts of extra line work here based on an awareness of A,B,C,D

		V+=vStep
	U+=uStep


