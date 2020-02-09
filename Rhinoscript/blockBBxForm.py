import rhinoscriptsyntax as rs

# obj = rs.GetObjects("Select block to query")

# def inputFunc():
#     objs = rs.GetObjects("Select solids", rs.filter.polysurface, preselect=True)
#     return objs

walls = rs.GetObjects("Select solids", rs.filter.polysurface, preselect=True)
blks = rs.GetObjects("Select blocks", rs.filter.instance)

def bbsolid(obj):
    if rs.IsBlockInstance(obj):
        arrMatrix = rs.BlockInstanceXform(obj)
        if arrMatrix is not None:
            pointId = rs.AddPoint([0,0,0])
            plane = rs.PlaneTransform(rs.WorldXYPlane(), arrMatrix)
            box = rs.BoundingBox(obj, plane)
            bb = rs.AddBox(box)
            # if box:
            #     for i, point in enumerate(box):
            #         rs.AddTextDot( i, point )
            
            xformscale = rs.XformScale((1.0,20.0,1.0))
            cob = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
            cob_inverse = rs.XformChangeBasis(plane, rs.WorldXYPlane())
            temp = rs.XformMultiply(xformscale, cob)
            xform = rs.XformMultiply(cob_inverse, temp)
            rs.TransformObjects(bb, xform)
            return bb

solids = bbsolid(blks)
print solids
print walls