import rhinoscriptsyntax as rs

objs = rs.GetObjects("Select surfaces", rs.filter.surface | rs.filter.polysurface, preselect=True)

def calcArea(srfs):
    areas = []
    for srf in srfs:
        areas.append(rs.SurfaceArea(srf)[0])
    totalArea = sum(areas)
    # totalAreaPy = totalArea/3.3058
    # print(area, areapy)
    # txt = rs.ClipboardText(area)
    return totalArea

def srfunion(objs):
    joinedsrfs = rs.BooleanUnion(objs)
    rs.SelectObjects(joinedsrfs)
    rs.Command("-_MergeAllFaces")
    rs.UnselectObjects(joinedsrfs)
    return joinedsrfs
    # print joinedsrfs
    # borders = [rs.DuplicateSurfaceBorder(srf) for srf in joinedsrfs]
    # print borders
    # newsrfs = []
    # for border in borders:
    #     if border and len(border)>1:
    #         cb = rs.CurveBooleanUnion(border)
    #         newsrfs.append(rs.AddPlanarSrf(cb))
    #         rs.DeleteObjects(cb)
    #     else:
    #         newsrfs.append(rs.AddPlanarSrf(border))
    # return newsrfs

def createCoverage(objs):
    plane = rs.WorldXYPlane()
    borders = [rs.DuplicateSurfaceBorder(obj) for obj in objs]
    matrix = rs.XformPlanarProjection(plane)
    projcrvs = rs.TransformObjects(borders, matrix, copy=False)
    if projcrvs and len(projcrvs)>1:
        cb = rs.CurveBooleanUnion(projcrvs)
        result = rs.AddPlanarSrf(cb)
        rs.DeleteObjects(cb)
    else:
        result = rs.AddPlanarSrf(projcrvs)
    if result: rs.DeleteObjects(projcrvs)
    designCoverageArea = calcArea(result)
    return designCoverageArea

def runTest():
    sitearea = float(rs.GetDocumentUserText("site area"))
    legalscr = float(rs.GetDocumentUserText("legal scr"))
    legalfar = float(rs.GetDocumentUserText("legal far"))
    designGFA = calcArea(objs)
    designFAR = designGFA/sitearea
    designCVA = createCoverage(objs)
    designSCR = designCVA/sitearea
    rs.SetDocumentUserText("design gfa", str(designGFA))
    rs.SetDocumentUserText("design far", str(designFAR))
    rs.SetDocumentUserText("design cva", str(designCVA))
    rs.SetDocumentUserText("design scr", str(designSCR))

runTest()
# print srfunion(objs)

# def createFloorArea(objs):
#     if objs and len(objs)>1: 
#         floors = rs.BooleanUnion(objs)
#         rs.SelectObjects(floors)
#         rs.Command("-_MergeAllFaces")
#         rs.UnselectObjects(floors)
#     else:
#         floors = objs
#     gfa = calcArea(floors)
#     return floors, gfa

# def srfunion(objs):
#     joinedsrfs = rs.BooleanUnion(objs)
#     print joinedsrfs
#     borders = [rs.DuplicateSurfaceBorder(srf) for srf in joinedsrfs]
#     print borders
#     newsrfs = []
#     for border in borders:
#         if border and len(border)>1:
#             cb = rs.CurveBooleanUnion(border)
#             newsrfs.append(rs.AddPlanarSrf(cb))
#             rs.DeleteObjects(cb)
#         else:
#             newsrfs.append(rs.AddPlanarSrf(border))
#     return newsrfs

# def createCoverage(objs):
#     plane = rs.WorldXYPlane()
#     borders = [rs.DuplicateSurfaceBorder(obj) for obj in objs]
#     matrix = rs.XformPlanarProjection(plane)
#     projcrvs = rs.TransformObjects(borders, matrix, copy=False)
#     if projcrvs and len(projcrvs)>1:
#         cb = rs.CurveBooleanUnion(projcrvs)
#         result = rs.AddPlanarSrf(cb)
#         rs.DeleteObjects(cb)
#     else:
#         result = rs.AddPlanarSrf(projcrvs)
#     if result: rs.DeleteObjects(projcrvs)
#     designCoverageArea = calcArea(result)
#     return designCoverageArea


# sitearea = float(rs.GetDocumentUserText("site area"))
# legalscr = float(rs.GetDocumentUserText("legal scr"))
# legalfar = float(rs.GetDocumentUserText("legal far"))

# floors = createFloorArea(objs)


# designGFA = floors[1]
# designFAR = designGFA/sitearea
# designCVA = createCoverage(floors[0])
# designSCR = designCVA/sitearea