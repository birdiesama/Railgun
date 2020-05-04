################################################################################
__Script__      = 'global_RG.general.module.xgen'
__Author__      = 'Weerapot Chaoman'
__Version__     = 1.01
__Date__        = 20200503
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

import pymel.core as pm
import xgenm as xg

class XGen(object):

    def __init__(self):
        super(XGen, self).__init__()

    def guide_to_curve(self):
        selection_list = pm.ls(sl = True)
        curve_grp_list = []
        for selection in selection_list:
            pm.select(selection)
            curve_list = pm.mel.eval('xgmCreateCurvesFromGuides(0, 0)')
            curve_grp = pm.listRelatives(curve_list, parent = True)[0]
            curve_grp.rename(selection.nodeName() + '_GDC')
            pm.parent(curve_grp, w = True)
            curve_grp_list.append(curve_grp)
        return curve_grp_list