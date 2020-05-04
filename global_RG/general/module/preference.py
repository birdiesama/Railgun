################################################################################
__Script__  = 'global_RG.general.module.preference'
__Author__  = 'Weerapot Chaoman'
__Version__ = 1.1
__Date__    = 20200503
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

import pymel.core as pm

class Preference(object):

    def __init__(self, *args, **kwargs):
        super(Preference, self).__init__(*args, **kwargs)

    def set_color_management(self, enable = True):
        pm.colorManagementPrefs(e = True, cme = enable)

    def toggle_color_management(self):
        if pm.colorManagementPrefs(q = True, cme = True):
            enable = False
        else:
            enable = True
        self.set_color_management(enable = enable)
