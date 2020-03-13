import rhinoscriptsyntax as rs

objs = rs.GetObjects('select objs', rs.filter.surface|rs.filter.curve|rs.filter.point, preselect=True)
grade = rs.GetString("toggle grade")

def setGrade(grade):
    if len(grade) == 0:
        return False
    else:
        return True

def srfPointZ(srf):
    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[1]/2.0
    v = domainV[1]/2.0
    point = rs.EvaluateSurface(srf, u, v)
    el = round(point.Z, 3)
    return [srf, el]

def crvPointZ(crv):
    domain = rs.CurveDomain(crv)
    t = domain[1]/2.0
    point = rs.EvaluateCurve(crv, t)
    el = round(point.Z, 3)
    return [crv, el]

def makePair(obj):
    if rs.IsCurve(obj):
        return crvPointZ(obj)
    elif rs.IsSurface(obj):
        return srfPointZ(obj)
    elif rs.IsPoint(obj):
        pt = rs.CreatePoint(obj)
        return [obj, round(pt.Z, 3)]
    else:
        pass

def groupByElevation(objs, isUG):
    pairs = map(makePair, objs)
    values = set(map(lambda x:x[1], pairs))
    newpairs = [[y for y in pairs if y[1]==x] for x in values]
    return sorted(newpairs, key=lambda x:x[0][1], reverse=isUG)

def setLevel(sortedpairs, isUG):
    for idx, pairs in enumerate(sortedpairs, start=1):
        grade = 'AG'
        if isUG: 
            idx = -idx
            grade = 'UG'
        # func = lambda x: rs.SetUserText(x[0], "level", str(idx))
        def func(x):
            rs.SetUserText(x[0], "level", str(idx))
            rs.SetUserText(x[0], "grade", grade)
        map(func, pairs)

    

def process(objs, grade):
    isUG = setGrade(grade)
    groups = groupByElevation(objs, isUG)
    setLevel(groups, isUG)

process(objs, grade)