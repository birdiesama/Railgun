'''
how to use
1. select controller you want to use as reference
2. shift+select placement
make sure you have the correct frame range
run the script
'''
import pymel.core as pm

start_frame = pm.playbackOptions(q = True, min = True)
end_frame = pm.playbackOptions(q = True, max = True)

selection_list = pm.ls(sl = True)

driver = selection_list[0]
driven = selection_list[1]

pm.currentTime(start_frame)
pos1 = pm.xform(driver, q = True, ws = True, rp = True)
pm.currentTime(end_frame)
pos2 = pm.xform(driver, q = True, ws = True, rp = True)

tx_val = (pos2[0]-pos1[0])*-1.0
ty_val = (pos2[1]-pos1[1])*-1.0
tz_val = (pos2[2]-pos1[2])*-1.0

pm.setKeyframe(driven.tx, value = 0.0, time = start_frame, inTangentType = "linear", outTangentType = "linear")
pm.setKeyframe(driven.ty, value = 0.0, time = start_frame, inTangentType = "linear", outTangentType = "linear")
pm.setKeyframe(driven.tz, value = 0.0, time = start_frame, inTangentType = "linear", outTangentType = "linear")
pm.setKeyframe(driven.tx, value = tx_val, time = end_frame, inTangentType = "linear", outTangentType = "linear")
pm.setKeyframe(driven.ty, value = ty_val, time = end_frame, inTangentType = "linear", outTangentType = "linear")
pm.setKeyframe(driven.tz, value = tz_val, time = end_frame, inTangentType = "linear", outTangentType = "linear")