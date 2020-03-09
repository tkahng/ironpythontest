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
    srfs = []
    for obj in objs:
        if rs.IsPolysurface(obj):
            faces = rs.ExplodePolysurfaces(obj)
            [srfs.append(face) for face in faces]
        else:
            srfs.append(obj)

    return rs.BooleanUnion(srfs)

def createCoverage(objs):
    rs.EnableRedraw(False)
    objs = rs.CopyObjects(objs)
    plane = rs.WorldXYPlane()
    joinedsrfs = srfunion(objs)
    designFloorArea = calcArea(joinedsrfs)
    matrix = rs.XformPlanarProjection(plane)
    projcrvs = rs.TransformObjects(joinedsrfs, matrix, copy=False)
    if projcrvs and len(projcrvs)>1:
        result = srfunion(projcrvs)
    else:
        result = projcrvs
    if result: rs.DeleteObjects(projcrvs)
    designCoverageArea = calcArea(result)
    rs.DeleteObjects(result)
    rs.EnableRedraw(True)
    return designCoverageArea, designFloorArea

siteKeys = ("site area", "legal scr", "legal far")

def runTest():
    areas = createCoverage(objs)
    sitearea = float(rs.GetDocumentUserText("site area"))
    legalscr = float(rs.GetDocumentUserText("legal scr"))
    legalfar = float(rs.GetDocumentUserText("legal far"))
    designGFA = areas[1]
    designFAR = designGFA/sitearea
    designCVA = areas[0]
    designSCR = designCVA/sitearea
    rs.SetDocumentUserText("design gfa", str(designGFA))
    rs.SetDocumentUserText("design far", str(designFAR))
    rs.SetDocumentUserText("design cva", str(designCVA))
    rs.SetDocumentUserText("design scr", str(designSCR))

def startupUserText():
    for key in siteKeys:
        rs.SetDocumentUserText(key, " ")

def startupValueCheck():
    test = []
    for key in siteKeys:
        try:
            float(rs.GetDocumentUserText("site area"))
            test.append(True)
        except:
            test.append(False)
    # print test
    if False in test: 
        return False
    else: 
        return True



def checkUserText():
    keylist = rs.GetDocumentUserText()
    # print keylist
    if keylist is None: 
        startupUserText()
    elif startupValueCheck()==False:
        return
    else:
        runTest()

checkUserText()
