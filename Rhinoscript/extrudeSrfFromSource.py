# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import userTextUtils

objs = rs.GetObjects('select srfs', rs.filter.surface, preselect=True)

def srfExtrude(srfs):
    rs.EnableRedraw(False)
    # for srf in srfs:
    rs.SelectObjects(srfs)
    rs.Command('_ExtrudeSrf _Pause')
    objs = rs.LastCreatedObjects()
    map(userTextUtils.copySourceLayer, objs, srfs)
    map(userTextUtils.copySourceData, objs, srfs)
    rs.EnableRedraw(True)

srfExtrude(objs)