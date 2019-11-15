# draw lines normal to surface
import rhinoscriptsyntax as rs

srf = rs.GetObjects("pick surface", 8)

numberUDivs= 20
numberVDivs= 50

uDomain = rs.SurfaceDomain(srf, 0)
vDomain = rs.SurfaceDomain(srf, 1)

uMin = uDomain[0]
uMax = uDomain[1]
vMin = vDomain[0]
vMax = vDomain[1]

uRange = uMax-uMin
vRange = vMax-vMin

uStep = uRange/numberUDivs
vStep = vRange/numberVDivs

U = uMin
while U < uMax:
	V = vMin
	while V<vMax:
		
		normal = rs.SurfaceNormal(srf, (U,V))
		scaledNormal = rs.VectorScale(normal, 15)
		pointOnSurface = rs.EvaluateSurface(srf, U,V)
		pointOffSurface = rs.VectorAdd(pointOnSurface, scaledNormal)
		rs.AddLine(pointOnSurface,pointOffSurface)
		V=V+vStep
	U = U + uStep


