import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects("Select a srf", rs.filter.surface, preselect=True)

