import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objects', preselect=True)
key = rs.GetString('key')
# objkeys = map(lambda x: rs.GetUserText(x, key), objs)
values = map(lambda x: rs.GetUserText(x, key), objs)
# print len(value)
# print type(value)
# print value[0]
# pairs = zip(objs, values)
# print pairs
def func(a,b):
    return [a, b]

pairs = map(func, objs, values)
setpairs = set(map(lambda x:x[1], pairs))
newpairs = [[y[0] for y in pairs if y[1]==x] for x in setpairs]
# sets = set(map(lambda x:x[1], pairs))

for x in newpairs: print len(x[0])
for x in newpairs: print type(x[0])

for x in newpairs:
    group = rs.AddGroup()
    print rs.AddObjectsToGroup(x, group)