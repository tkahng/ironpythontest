import rhinoscriptsyntax as rs
# !-RunPythonScript "objectsBottomFace.py"

def inputFunc():
    objs = rs.GetObjects("Select polysurface to explode", rs.filter.polysurface, preselect=True)
    return objs

def bottomFaceBndry(obj):
    bndry = []
    objLayer = rs.ObjectLayer(obj)
    # if rs.IsPolysurface(obj):
    #     faces = rs.ExplodePolysurfaces( obj )
    faces = rs.ExplodePolysurfaces(obj)
    for face in faces:
        if rs.IsSurface(face):
            domainU = rs.SurfaceDomain(face, 0)
            domainV = rs.SurfaceDomain(face, 1)
            u = domainU[1]/2.0
            v = domainV[1]/2.0
            point = rs.EvaluateSurface(face, u, v)
            param = rs.SurfaceClosestPoint(face, point)
            normal = rs.SurfaceNormal(face, param)
            # print normal
            if normal.Z == -1:
                rs.ObjectLayer(face, objLayer)
                # rs.SetUserText(face, "tempTag", 1)
                bndry.append(face)
            else:
                rs.DeleteObject(face)
        else:
            pass
    
    # return map(lambda x: rs.ObjectLayer(x, objLayer), bndry)
    return bndry
    # print bndry

def calcArea(srfs):
    areas = []
    for srf in srfs:
        areas.append(rs.SurfaceArea(srf)[0])
    totalArea = sum(areas)
    totalAreaPy = totalArea/3.3058
    print totalArea, totalAreaPy
    txt = rs.ClipboardText(totalArea)

def outputFunc(objs):
    rs.EnableRedraw(False)
    bottomFaces = []
    for obj in objs:
        resultFaces = bottomFaceBndry(obj)
        for resultFace in resultFaces:
            bottomFaces.append(resultFace)
    rs.SelectObjects(bottomFaces)
    group = rs.AddGroup()
    rs.AddObjectsToGroup(bottomFaces, group)
    rs.EnableRedraw(True)
    return bottomFaces

def returnFaces():
    objs = inputFunc()
    rs.UnselectAllObjects()
    outputsrfs = outputFunc(objs)
    calcArea(outputsrfs)

if __name__ == '__main__':
    returnFaces()