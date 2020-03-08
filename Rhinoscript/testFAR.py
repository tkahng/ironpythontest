import rhinoscriptsyntax as rs

objs = rs.GetObjects("Select surfaces", rs.filter.surface, preselect=True)




if faces: rs.DeleteObjects(faces)

def calcArea(srfs):
    areas = []
    for srf in srfs:
        areas.append(rs.SurfaceArea(srf)[0])
    totalArea = sum(areas)
    totalAreaPy = totalArea/3.3058
    print(area, areapy)
    txt = rs.ClipboardText(area)
    return totalArea

# def testfar():

sitearea = rs.GetDocumentUserText("site area")

def testfar(sitearea, designgfa):
    if sitearea.type
    designfar = designgfa/sitearea
    


