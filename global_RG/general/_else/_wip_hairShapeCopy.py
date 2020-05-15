import pymel.core as pm

def getDistance(point1, point2):
    distance = ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2) ** 0.5
    return distance

group_list = pm.ls(sl=True)
driver_group = group_list[0]
driven_group = group_list[1]
driver_group_children = driver_group.listRelatives(ad = True, type = 'nurbsCurve')

driven_group_children = driven_group.listRelatives(ad = True, type = 'nurbsCurve')
for driven in driven_group_children:
    if driven.isIntermediate():
        driven_group_children.remove(driven)

driver_pos_list = []

for driver in driver_group_children:
    pos = pm.xform('{driver}.cv[0]'.format(driver = driver), q = True, ws = True, t = True)
    driver_pos_list.append([driver, pos])

for driven in driven_group_children:
    driven_pos = pm.xform('{driven}.cv[0]'.format(driven = driven), q = True , ws = True, t = True)
    driven_distance_list = []
    for driver_pos in driver_pos_list:
        driven_distance_list.append([getDistance(driven_pos, driver_pos[1]), driver_pos[0]])
    driven_distance_list.sort()
    driver = driven_distance_list[0][1]

    degree = pm.getAttr(driver + '.degree')
    spans = pm.getAttr(driver + '.spans')
    cv = degree + spans

    for index in range (0, cv+1):
        pos = pm.xform('{driver}.cv[{index}]'.format(driver = driver, index = index), q = True , ws = True, t = True)
        pm.xform('{driven}.cv[{index}]'.format(driven = driven, index = index), ws = True, t = pos)
