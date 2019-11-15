import rhinoscriptsyntax as rs

joints = []
legs = []
legsl = []

jNr = rs.GetInteger(“Enter the number of joints:”,4,2,8)
for i in range(0, jNr): joints.append(rs.GetPoint(“Locate joint nr.”+str(i)))
rs.AddPoints(joints)
goal = rs.GetPoint(“Locate the goal”)
rs.AddPoint(goal)
precision = rs.GetReal(“Enter the precision of the approximation:”,0.1,0.001,1)
arm = rs.AddPolyline(joints)
base = joints[0]
legsl = rs.ExplodeCurves(arm, True)
for l in legsl: legs.append(rs.CurveLength(l))
joints.insert(jNr, goal)
legs.append(0)
error = rs.Distance(goal, joints[jNr-1])

def chain(ch, lh, i):
    while i > 0:
        temp1 = rs.AddLine(ch[i], ch[i-1])
    if lh[i-1] > 0: temp2 = rs.EvaluateCurve(temp1, lh[i-1])
    if lh[i-1] == 0: temp2 = ch[i]
    ch[i-1] = temp2
    #rs.DeleteObject(temp1)
    i = i - 1
    return ch

iteration = 0
while error > precision:
    chain(joints, legs, jNr)
del joints[jNr]
joints.reverse()
joints.insert(jNr, base)
del legs[jNr-1]
legs.reverse()
legs.insert(jNr-1,0)
chain(joints, legs, jNr)
rs.AddPolyline(joints)
del joints[jNr]
joints.reverse()
joints.insert(jNr, goal)
del legs[jNr-1]
legs.reverse()
legs.insert(jNr-1,0)
error = rs.Distance(goal, joints[jNr-1])
iteration = iteration + 1
print “iteration #”+str(iteration)+”: Error=”+str(error)
if iteration > 10: break # Safety exit