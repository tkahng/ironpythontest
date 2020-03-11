import rhinoscriptsyntax as rs


def inputVector():
    p1 = rs.GetPoint("Pick first point")
    if p1:
        p2 = rs.GetPoint("Pick second point", p1)
    vec = p2 - p1
    return vec

def toggleStop():
    toggle = rs.GetString("toggle stop")
    if len(toggle) == 0:
        return False
    else:
        return True


stop = False
vector = rs.CreateVector(0.0, 0.0, 0.0)
vec = inputVector()
while stop is False:
    # vec = inputVector()
    vector = vector + vec
    # print vector
    objs = rs.GetObjects("Select objs")
    rs.MoveObjects( objs, vector)
    stop = toggleStop()