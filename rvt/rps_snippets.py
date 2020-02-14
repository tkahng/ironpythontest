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