import pymel.core as pm

selection_list = pm.ls(sl = True)
fol_shape_list = pm.listRelatives(selection_list, ad = True, type = 'follicle')


meshShape = pm.PyNode('skinPink_C_dodge_0001_mid_GES_folDriverShape')

for fol_shape in fol_shape_list:
    inputWorldMatrix_input = pm.listConnections(fol_shape.inputWorldMatrix, plugs = True)[0]
    inputMesh_input = pm.listConnections(fol_shape.inputMesh, plugs = True)

    fol_shape.inputWorldMatrix.disconnect()
    fol_shape.inputMesh.disconnect()

    meshShape.worldMatrix[0] >> fol_shape.inputWorldMatrix
    meshShape.outMesh >> fol_shape.inputMesh

###

import re

class NaturalSort(object):
    def __init__(self, *args, **kwargs):
        super(NaturalSort, self).__init__(*args, **kwargs)

    def convert_key_elem(self, input):
        if input.isdigit(): return int(input)
        else: return input.lower()

    def split_key(self, key):
        return_list = []
        key = str(key)
        for elem in re.split('([0-9]+)', key):
            return_list.append(self.convert_key_elem(elem))
        return return_list

    def natural_sort(self, list):
        return sorted(list, key = self.split_key)

ns = NaturalSort()

import pymel.core as pm

selection_list = pm.ls(sl = True)
driver, driven = selection_list

driver_curve_list = pm.listRelatives(driver, ad = True, type = 'nurbsCurve')
driver_curve_list = pm.listRelatives(driver_curve_list, parent = True)
driver_curve_list = list(set(driver_curve_list))
driver_curve_list = ns.natural_sort(driver_curve_list)

driven_curve_list = pm.listRelatives(driven, ad = True, type = 'nurbsCurve')
driven_curve_list = pm.listRelatives(driven_curve_list, parent = True)
driven_curve_list = list(set(driven_curve_list))
driven_curve_list = ns.natural_sort(driven_curve_list)

for driver, driven in zip(driver_curve_list, driven_curve_list):
    driven.rename(driver.nodeName().split('tempCurve')[0] + 'sim')

#####

import pymel.core as pm

selection_list = pm.ls(sl = True)
for selection in selection_list:
    selection.rename(selection.nodeName().split('tempCurve')[0] + 'input')
