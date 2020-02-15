from pyrevit import revit, DB

revit.db.query.get_param_value

cws = [w for w in wc if w.WallType.Kind.ToString() == 'Curtain']

wc = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Walls).WhereElementIsNotElementType()



# Selecting Curtainwalls
from System.Collections.Generic import List
wc = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
cws = [w.Id for w in wc if w.WallType.Kind.ToString() == 'Curtain']
uidoc.Selection.SetElementIds(List[DB.ElementId](cws))


def get_walls():
    """retrieve wall from selection set"""
    return [x for x in revit.get_selection() if isinstance(x, DB.Wall)]


def get_section_viewfamily():
    return revit.doc.GetDefaultElementTypeId(
        DB.ElementTypeGroup.ViewTypeSection
        )

# curtainwall dim debug

wall = el



def isParallel(v1,v2):
    return v1.CrossProduct(v2).IsAlmostEqualTo(DB.XYZ(0,0,0))
    
line = wall.Location.Curve
lineDir = line.GetEndPoint(1) - line.GetEndPoint(0)

refArray = DB.ReferenceArray()

# doc = DocumentManager.Instance.CurrentDBDocument

options = DB.Options()
options.ComputeReferences = True
options.IncludeNonVisibleObjects = True

geoElement = wall.get_Geometry(options)

#get side references
for obj in geoElement:
    if isinstance(obj,DB.Solid):
        for f in obj.Faces:
            faceNormal = f.FaceNormal
            if isParallel(faceNormal,lineDir):
                refArray.Append(f.Reference)



from pyrevit import revit, DB

def cwrefs(cw):

    refArray = DB.ReferenceArray()
    faces = []
    options = DB.Options()
    options.ComputeReferences = True
    options.IncludeNonVisibleObjects = True

    geoElement = cw.get_Geometry(options)

    for obj in geoElement:
        if isinstance(obj,DB.Solid):
            for f in obj.Faces:
                refArray.Append(f.Reference)
    return refArray

