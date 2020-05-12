################################################################################
__Script__  = 'utils_RG.utils_nucleus'
__Author__	= 'Weerapot Chaoman'
__Version__	= 1.20
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

##################
''' nCache '''
##################
def create_nCache_btnCmd():
    selection_list = pm.ls(sl=True)
    gen.nCache_create(selection_list)

##################
''' nConstraint '''
##################
def toggle_nCon_display_connection_btnCmd():

    selection_list = pm.ls(sl=True)

    display_stat_list = []
    for selection in selection_list:
        display_stat_list.append(gen.get_display_connections_stat(selection))
    display_stat_list = list(set(display_stat_list))

    if len(display_stat_list) == 1:
        enable = not display_stat_list[0]
    else:
        enable = True

    for selection in selection_list:
        gen.toggle_nCon_display_connection(selection, enable = enable)

##################
''' nucleus '''
##################
def make_nRigid_btnCmd() :
    selection_list = pm.ls(sl=True)
    nRigid_list = []
    for selection in selection_list :
        nRigid = gen.make_nRigid(selection)
        nRigid_list.append(nRigid)
    return nRigid_list

def __1__enable_nObject_btnCmd():
    selection_list = pm.ls(sl = True)
    gen.toggle_nObject_enable(selection_list, enable = True)

def __2__disable_nObject_btnCmd():
    selection_list = pm.ls(sl = True)
    gen.toggle_nObject_enable(selection_list, enable = False)

def __3__select_sim_members_from_nucleus_btnCmd():
    selection_list = pm.ls(sl = True, type='nucleus')
    to_select_list = gen.get_sim_object_from_nucleus(selection_list)
    if to_select_list:
        pm.select(to_select_list)

def __4__select_nucleus_from_sim_members_btnCmd():
    selection_list = pm.ls(sl = True)
    to_select_list = gen.get_nucleus_from_members(selection_list)
    if to_select_list:
        pm.select(to_select_list)

def __5__suppress_script_editor_warnings_btnCmd():
    pm.scriptEditorInfo(suppressWarnings = True, suppressInfo = True, suppressErrors = True)

def __6__upsuppress_script_editor_warnings_btnCmd():
    pm.scriptEditorInfo(suppressWarnings = False, suppressInfo = False, suppressErrors = False)
