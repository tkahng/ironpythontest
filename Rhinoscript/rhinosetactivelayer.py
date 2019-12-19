import rhinoscriptsyntax as rs

layer = rs.GetLayer("Select Layer", rs.CurrentLayer(), True, True)
if layer: rs.CurrentLayer(layer)
