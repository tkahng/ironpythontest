import rhinoscriptsyntax as rs 
import random

v1 = random.uniform(-100,100)
v2 = random.uniform(-100,100)
v3 = random.uniform(-100,100)
v4 = random.uniform(-100,100)
v5 = random.uniform(-100,100)
v6 = random.uniform(-100,100)
v7 = random.uniform(-100,100)
v8 = random.uniform(-100,100)
v9 = random.uniform(-100,100)

myPointA = [v1,v2,v3]
myPointB = [v4,v5,v6]
myPointC = [v7,v8,v9]

rs.AddInterpCurve([myPointA,myPointB,myPointC], 1)
rs.AddInterpCurve([myPointA,myPointB,myPointC], 3)

