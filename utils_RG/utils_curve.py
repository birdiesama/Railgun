################################################################################
__Script__  = 'utils_RG.utils_curve'
__Author__	= 'Weerapot Chaoman'
__Version__	= 1.10
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

class QuickGuiChild(object):
    def __init__(self):
        super(QuickGuiChild, self).__init__()
        self.column = 2

gen = general.General()

def __1__select_first_cv_btnCmd(*args, **kwargs):
    selection_list = pm.ls(sl = True)
    curve_shape_list = pm.listRelatives(selection_list, ad = True, type = 'nurbsCurve')
    curve_list = pm.listRelatives(curve_shape_list, parent = True)
    curve_list = list(set(curve_list))
    to_select_list = gen.get_curve_first_cv(curve_list)
    pm.select(to_select_list)

def __2__select_last_cv_btnCmd(*args, **kwargs):
    selection_list = pm.ls(sl = True)
    curve_shape_list = pm.listRelatives(selection_list, ad = True, type = 'nurbsCurve')
    curve_list = pm.listRelatives(curve_shape_list, parent = True)
    curve_list = list(set(curve_list))
    to_select_list = gen.get_curve_last_cv(curve_list)
    pm.select(to_select_list)

def __3__randomize_curve_color_btnCmd(*args, **kwargs):
    selection_list = pm.ls(sl = True)
    curve_shape_list = pm.listRelatives(selection_list, ad = True, type = 'nurbsCurve')
    curve_list = pm.listRelatives(curve_shape_list, parent = True)
    curve_list = list(set(curve_list))
    gen.random_curve_color(curve_list, enable = True)

def __4__disable_curve_color_btnCmd(*args, **kwargs):
    selection_list = pm.ls(sl = True)
    curve_shape_list = pm.listRelatives(selection_list, ad = True, type = 'nurbsCurve')
    curve_list = pm.listRelatives(curve_shape_list, parent = True)
    curve_list = list(set(curve_list))
    gen.random_curve_color(curve_list, enable=False)
