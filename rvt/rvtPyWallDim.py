"""Create section parallel to the plane of selected walls or planar element."""
#pylint: disable=import-error,invalid-name,broad-except
from pyrevit import revit, DB
from pyrevit import script

# adapted from https://thebuildingcoder.typepad.com/blog/2012/06/create-section-view-parallel-to-wall.html
__author__ = 'Source: Jeremy Tammik\nAdapted by: {{author}}'

logger = script.get_logger()
output = script.get_output()


def get_walls():
    """retrieve wall from selection set"""
    return [x for x in revit.get_selection() if isinstance(x, DB.Wall)]













doc_section_type = get_section_viewfamily()

with revit.Transaction("Create Parallel Section"):
    for selected_wall in get_cw():
        create_section(selected_wall, doc_section_type)
