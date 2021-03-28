################################################################################
__Script__      = 'global_RG.ui.core'
__Author__      = 'Weerapot Chaoman'
__Version__     = 1.00
__Date__        = 20200504
################################################################################
import os, sys, importlib
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
module_list = []
module_list.append(['global_RG.ui.module', 'qt_ui', 'qt_ui'])
if __project__ in __self_path__:
    local_path = __self_path__.split(__project__)[0]
    if not local_path in sys.path:
        sys.path.insert(0, local_path)
for module_data in module_list:
    parent, module, as_name = module_data
    cmd = 'import '
    if __project__ in __self_path__:
        cmd += __project__ + '.'
    if parent:
        cmd += parent + '.'
    cmd += module + ' as ' + as_name + ';'
    cmd += 'importlib.reload(' + as_name + ');'
    exec(cmd)
################################################################################
import random, re
import pymel.core as pm
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
from collections import OrderedDict
################################################################################

class UI(
	qt_ui.Qt_UI,
    ):

    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)
