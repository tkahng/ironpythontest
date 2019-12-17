import rhinoscriptsyntax as rs
objs = rs.GetObjects("Pick curves to loft", rs.filter.curve)
# if objs: rs.AddLoftSrf(objs)
curve = rs.AddLine((5,0,0), (10,0,10))
surface = rs.AddSrfPt([(0,0,0), (5,0,0), (5,5,0), (0,5,0)])
rs.ExtrudeSurface(surface, curve)

