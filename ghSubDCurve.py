"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "인시공현장PC"
__version__ = "2019.10.28"

import clr
clr.AddReference('RhinoCommon')

import Rhino

Rhino.geo

Rhino.Geometry.Point3d.Add

for j in len(y):
    cPoints = []
    
    for i in len(x)-1:
        oneQuarterPoint = 0.75 * x[i] + 0.25 * x[i+1]
        cPoints.Add(oneQuarterPoint)
        
        threeQuarterPoint = 0.25 * x[i] + 0.75 * x[i+1]
        cPoints.Add(threeQuarterPoint)