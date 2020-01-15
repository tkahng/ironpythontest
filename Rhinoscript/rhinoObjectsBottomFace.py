import rhinoscriptsyntax as rs

def inputFunc():
    objs = rs.GetObjects("Select polysurface to explode", rs.filter.polysurface, preselect=True)
    return objs
    rs.UnselectObjects(objs)

def bottomFaceBndry(obj):
    bndry = []
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
                bndry.append(face)
            else:
                rs.DeleteObject(face)
        else:
            pass
    return bndry
    print bndry

def outputFunc(objs):
    rs.EnableRedraw(False)
    bottomFaces = []
    for obj in objs:
        resultFaces = bottomFaceBndry(obj)
        for resultFace in resultFaces:
            bottomFaces.append(resultFace)
    rs.SelectObjects(bottomFaces)
    rs.EnableRedraw(True)

def returnFaces():
    objs = inputFunc()
    outputFunc(objs)

if __name__ == '__main__':
    returnFaces()