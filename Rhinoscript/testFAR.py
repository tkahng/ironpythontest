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
    borders = [rs.DuplicateSurfaceBorder(joinedsrf) for joinedsrf in objs]
    # rs.SelectObjects(joinedsrfs)
    # rs.Command("-_MergeAllFaces")
    # rs.UnselectObjects(joinedsrfs)
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

siteKeys = ("site area", "legal scr", "legal far")

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


def checkUserText():
    keylist = rs.GetDocumentUserText()
    ready = True
    for siteKey in siteKeys:
        if siteKey not in keylist:
            ready == False
            rs.SetDocumentUserText(siteKey, "default")
        elif rs.GetDocumentUserText(siteKey) == "default":
            ready == False

    if ready == True:
        runTest()

# checkUserText()
runTest()
# print srfunion(objs)
