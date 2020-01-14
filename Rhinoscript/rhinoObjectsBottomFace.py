import rhinoscriptsyntax as rs

# rs.EnableRedraw(False)

objs = rs.GetObjects("Select polysurface to explode", rs.filter.polysurface, preselect=True)
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

bottomFaces = []

for obj in objs:
    resultFaces = bottomFaceBndry(obj)
    for resultFace in resultFaces:
        bottomFaces.append(resultFace)

rs.SelectObjects(bottomFaces)

# print bottomFaces


    # for bnd in bndry:
    #     area = rs.SurfaceArea(bnd)[0]
    #     areapy = area/3.3058
    #     print area, areapy
    #     txt = rs.ClipboardText(area)

    # return bndry

# if faces: rs.DeleteObjects(faces)