import rhinoscriptsyntax as rs

points = rs.GetObjects("pick points to map",1)
referenceSurface = rs.GetObject("pick reference surface",8)
destinationSurface = rs.GetObject("pick destination surface",8)


listOfDestinationPoints = []

for myPoint in points:

	UV = rs.SurfaceClosestPoint(referenceSurface, myPoint)
	
	U = UV[0]
	V = UV[1]
	


	domainUReferene= rs.SurfaceDomain (referenceSurface, 0)
	domainVReferene= rs.SurfaceDomain (referenceSurface, 1)

	rangeUReference = domainUReferene[1]-domainUReferene[0]
	rangeVReference = domainVReferene[1]-domainVReferene[0]

	relativeU = (U-domainUReferene[0]) / rangeUReference
	relativeV = (V-domainVReferene[0]) / rangeVReference

	#print (relativeU)
	#print (relativeV)
	
	
	domainUDestination = rs.SurfaceDomain(destinationSurface, 0)
	domainVDestination = rs.SurfaceDomain(destinationSurface, 1)
	
	rangeUDestination = domainUDestination[1]-domainUDestination[0]
	rangeVDestination = domainVDestination[1]-domainVDestination[0]


	absoluteU = relativeU * rangeUDestination + domainUDestination[0]
	absoluteV = relativeV * rangeVDestination + domainVDestination[0]


	pointOnDestination = rs.EvaluateSurface(destinationSurface, absoluteU, absoluteV)
	
	listOfDestinationPoints.append(pointOnDestination)
	rs.AddPoint(pointOnDestination)
	



#modify this script to make it a function so that the points can be pulled from curves and then the curves reconstructed




