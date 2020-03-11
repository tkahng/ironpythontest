import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objects', preselect=True)

keys = 'usage function'

def Func(x):
    trp.valuesFromLayer(x)
    trp.setValueByLayer(x,keys)
    trp.setAreaValue(x)

def applyFunc(objs):
    map(Func, objs)

if objs:
    applyFunc(objs)