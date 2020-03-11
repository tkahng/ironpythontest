import Rhino
import scriptcontext as sc

def test_willem():
    
    filter = Rhino.DocObjects.ObjectType.PolysrfFilter
    rc, objref = Rhino.Input.RhinoGet.GetOneObject("Select a polysurface", False, filter)
    if not objref or rc != Rhino.Commands.Result.Success: 
        return
        
    brep = objref.Brep()
    if not brep:
        return
        
    for edge in brep.Edges:
        if edge.Valence == Rhino.Geometry.EdgeAdjacency.Naked:
            inner = False
            for ti in edge.TrimIndices():
                loop = brep.Trims[ti].Loop
                if loop.LoopType == Rhino.Geometry.BrepLoopType.Inner:
                    sc.doc.Objects.AddCurve(edge.DuplicateCurve())
                    break
                
test_willem()