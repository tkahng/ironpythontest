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

# def testfar():

sitearea = float(rs.GetDocumentUserText("site area"))
legalscr = float(rs.GetDocumentUserText("legal scr"))
legalfar = float(rs.GetDocumentUserText("legal far"))

designgfa = calcArea(objs)
designfar = designgfa/sitearea


# print rs.DocumentDataCount()
rs.SetDocumentUserText("design gfa", str(designgfa))
rs.SetDocumentUserText("design far", str(designfar))

# def getBorders(objs):
#     crvs = []
#     for obj in

def createCoverage(objs):
    plane = rs.WorldXYPlane()
    borders = [rs.DuplicateSurfaceBorder(obj) for obj in objs]
    matrix = rs.XformPlanarProjection(plane)
    projcrvs = rs.TransformObjects(borders, matrix, copy=False)
    if projcrvs and len(projcrvs)>1:
        result = rs.CurveBooleanUnion(projcrvs)
        if result: rs.DeleteObjects(projcrvs)
    return result

    # return borders

# def createCoverage(objs):
#     plane = rs.WorldXYPlane()
#     # borders = [rs.DuplicateSurfaceBorder(obj) for obj in objs]
#     matrix = rs.XformPlanarProjection(plane)
#     # projsrfs = rs.TransformObjects(objs, matrix, copy=False)
#     projsrfs = rs.BooleanUnion(rs.TransformObjects(objs, matrix, copy=False), delete_input=True)
#     rs.SelectObjects(projsrfs)
#     rs.Command("reparameterize a")
#     # if projcrvs and len(projcrvs)>1:
#     #     result = rs.CurveBooleanUnion(projcrvs)
#     #     if result: rs.DeleteObjects(projcrvs)
#     # return result

#     # return borders

createCoverage(objs)

# print designfar
# def testfar(sitearea, designgfa):
#     if sitearea.type
#     designfar = designgfa/sitearea
    


