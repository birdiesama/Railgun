################################################################################
__Script__	= 'utils_RG.utils_camera'
__Author__	= 'Weerapot Chaoman'
__Version__ = 1.40
__Date__	= 20200512
################################################################################
import os, sys
import pymel.core as pm
################################################################################
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
class QuickGuiChild(object):
    def __init__(self):
        super(QuickGuiChild, self).__init__()
        self.column = 2
################################################################################
module_list = []
module_list.append(['global_RG.general', 'core', 'general'])
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
    cmd += 'reload(' + as_name + ');'
    exec(cmd)
################################################################################

gen = general.General()

def __010__toggle_resolution_gate_btnCmd():
    gen.toggle_resolution_gate()

def __011__toggle_pan_zoom_lock_btnCmd():
    gen.toggle_pan_zoom_lock()

def __020__toggle_viewport_renderer_btnCmd():
    gen.toggle_viewport_renderer()

def __021__toggle_anti_aliase_btnCmd():
    gen.toggle_anti_aliase()

def __030__toggle_color_management_btnCmd():
    gen.toggle_color_management()

def playblast_btnCmd():
    gen.tempt_playblast()

def view_fit_btnCmd():
    selection_list = pm.ls(sl=True)
    selection_shape_list = []
    for selection in selection_list:
        selection_shape_list.append(gen.get_visible_shape(selection))
    pm.viewFit(selection_shape_list)
