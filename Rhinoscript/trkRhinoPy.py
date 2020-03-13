# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 

def setSourceLayer(obj, source):
    sourceLayer = rs.ObjectLayer(source)
    rs.SetUserText(obj, 'source Layer', sourceLayer)

def copySourceLayer(obj, source):
    sourceLayer = rs.ObjectLayer(source)
    rs.ObjectLayer(obj, sourceLayer)

def getSourceKeys(source):
    if rs.IsUserText(source) == 0:
        print 'no keys'
        return
    return [ x for x in rs.GetUserText(source) if "BakeName" not in x ]

def sourceKeyValue(source):
    keys = getSourceKeys(source)
    values = map(lambda x: rs.GetUserText(source, x), keys)
    return keys, values

def copySourceData(obj, source):
    keyValue = sourceKeyValue(source)
    print keyValue
    map(lambda x, y: rs.SetUserText(obj, x, y), keyValue[0], keyValue[1])

def valuesFromLayer(obj):
    layer = rs.ObjectLayer(obj)
    if "::" in layer:
        layer = layer.split("::")
        layer = layer[1]
    keys = layer.split()
    return keys

def setValueByLayer(obj, keys):
    # keys = 'usage function'
    keys = keys.split()
    values = valuesFromLayer(obj)
    map(lambda x,y: rs.SetUserText(obj, x, y), keys, values)

def setAreaValue(obj):
    area = rs.SurfaceArea(obj)[0]
    area = round(area, 2)
    rs.SetUserText(obj, 'area', str(area))

def boolToggle(input):
    if len(input) == 0:
        return False
    else:
        return True


def getBottomFace(obj):
    faces = rs.ExplodePolysurfaces(obj)
    output = []
    [output.append(face) if getSrfNormal(face).Z == -1 else rs.DeleteObject(face) for face in faces]
    return output

def getSrfNormal(srf):
    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[1]/2.0
    v = domainV[1]/2.0
    point = rs.EvaluateSurface(srf, u, v)
    param = rs.SurfaceClosestPoint(srf, point)
    return rs.SurfaceNormal(srf, param)
        

def offsetInside(crv, dist):
    rs.SimplifyCurve(crv)
    centroid = rs.CurveAreaCentroid(crv)
    return rs.OffsetCurve(crv, centroid[0], dist)

def brepGetZ(obj):
    box = rs.BoundingBox(obj)
    minZ = box[0].Z
    maxZ = box[-1].Z
    height = maxZ - minZ
    return round(height, 2)

"""Level Tools"""

def srfPtZPair(srf):
    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[1]/2.0
    v = domainV[1]/2.0
    point = rs.EvaluateSurface(srf, u, v)
    el = round(point.Z, 3)
    return [srf, el]

def crvPtZpair(crv):
    domain = rs.CurveDomain(crv)
    t = domain[1]/2.0
    point = rs.EvaluateCurve(crv, t)
    el = round(point.Z, 3)
    return [crv, el]

def setObjZPair(obj):
    if rs.IsCurve(obj):
        return crvPtZpair(obj)
    elif rs.IsSurface(obj):
        return srfPtZPair(obj)
    elif rs.IsPoint(obj):
        pt = rs.CreatePoint(obj)
        return [obj, round(pt.Z, 3)]
    else:
        pass

def groupByElevation(objs, isUG):
    pairs = map(setObjZPair, objs)
    values = set(map(lambda x:x[1], pairs))
    newpairs = [[y for y in pairs if y[1]==x] for x in values]
    return sorted(newpairs, key=lambda x:x[0][1], reverse=isUG)

def setLevel(sortedpairs, isUG, func):
    for idx, pairs in enumerate(sortedpairs, start=1):
        grade = 'AG'
        if isUG: 
            idx = -idx
            grade = 'UG'
        map(lambda x: func(x, idx, grade), pairs)

def setDictforDatum(x, idx, grade):
    keys = 'level grade elevation'
    keys = keys.split()
    vals = [idx, grade, str(x[1])]
    lvldict = dict(zip(keys, vals))
    rs.SetUserText(x[0], 'lvldict', lvldict)

def setLevelforObj(x, idx, grade):
    rs.SetUserText(x[0], "level", str(idx))
    rs.SetUserText(x[0], "grade", grade)    

def setLevelforDatum(x, idx, grade):
    rs.SetUserText(x[0], "level", str(idx))
    rs.SetUserText(x[0], "grade", grade) 
    rs.SetUserText(x[0], "elevation", str(x[1]))