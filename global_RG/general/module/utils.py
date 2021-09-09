################################################################################
__Script__          = 'global_RG.general.module.utils'
__Author__          = 'Weerapot Chaoman'
__Version__         = 1.0
__Date__            = 20200605
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import pymel.core as pm
import maya.cmds as mc
################################################################################

class Utils(object):

    def __init__(self):
        super(Utils, self).__init__()

    ######### Contraint #########

    def quick_par_con(self, driver, driven, mo=False, name=None):
        par_con = pm.parentConstraint(driver, driven, mo = mo, skipRotate = 'none', skipTranslate = 'none')
        if name:
            par_con.rename(name)
        else:
            par_con.rename(driven.stripNamespace() + '_parCon')
        return par_con

    def quick_point_con(self, driver, driven, mo=False, name=None):
        point_con = pm.pointConstraint(driver, driven, mo = mo, skip = 'none')
        if name:
            point_con.rename(name)
        else:
            point_con.rename(driven.stripNamespace() + '_pointCon')
        return point_con