################################################################################
__Script__	= 'utils_RG.utils'
__Author__	= 'Weerapot Chaoman'
__Version__	= 4.50
__Date__	= 20210327
################################################################################
import os, sys, random, re, importlib
import pymel.core as pm
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
from collections import OrderedDict
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
    cmd += 'importlib.reload(' + as_name + ');'
    exec(cmd)
################################################################################

##############################
''' GENERAL START '''
##############################

gen = general.General()

def __000__cluster_from_soft_selection_btnCmd():
    gen.create_soft_cluster()

def __001__cluster_group_btnCmd():
    selection_list = pm.ls(sl=True)
    gen.make_cluster_group(selection_list)

def __005__get_driver_attr_btnCmd():
    global cAttr_driver_attr_list
    cAttr_driver_attr_list = []
    cAttr_driver_attr_list = gen.get_selected_attributes()

def __006__connect_to_driven_attr_btnCmd():
    cAttr_driven_attr_list = gen.get_selected_attributes()
    if len(cAttr_driver_attr_list) == len(cAttr_driven_attr_list):
        for driver, driven in zip(cAttr_driver_attr_list, cAttr_driven_attr_list):
            driver >> driven
    else:
        if len(cAttr_driver_attr_list) == 1:
            driver = cAttr_driver_attr_list[0]
            for driven in cAttr_driven_attr_list:
                driver >> driven

def __010__copy_blendshape_weight_btnCmd(*args, **kwargs):
    blendshape_list = pm.ls(sl = True, type = 'blendShape')
    mesh_shape_list = gen.get_blendshape_member(blendshape_list, type = 'mesh')
    # mesh_shape_list = pm.listConnections(blendshape_list, type = 'mesh', destination = True, source = False)
    blendshape = blendshape_list[0]

    global cBsn_bsn_data_list
    cBsn_bsn_data_list = []
    
    for mesh_shape in mesh_shape_list:
        base_weight, iTarget_weight, src_total_vertices = gen.blendshape_get_weight(mesh_shape, blendshape)
        cBsn_bsn_data_list.append([base_weight, iTarget_weight, src_total_vertices])

def __011__paste_blendshape_weight_btnCmd(*args, **kwargs):
    blendshape_list = pm.ls(sl = True, type = 'blendShape')
    mesh_shape_list = gen.get_blendshape_member(blendshape_list, type = 'mesh')
    #mesh_shape_list = pm.listConnections(blendshape_list, type = 'mesh', destination = True, source = False)
    blendshape = blendshape_list[0]
    for mesh_shape in mesh_shape_list:
        for bsn_data in cBsn_bsn_data_list:
            gen.blendshape_set_weight(mesh_shape, blendshape, bsn_data[0], bsn_data[1], bsn_data[2])

def __012__quick_blendshape_btnCmd():
    selection_list = pm.ls(sl = True)
    driver = selection_list[0]
    driven_list = selection_list[1:]
    blendshape_list = []

    for driven in driven_list:
        blendshape = gen.quick_blendshape(driver, driven)
        blendshape_list.append(blendshape)

    return blendshape_list ;

def reorder_children_btnCmd():
    group_list = pm.ls(sl = True)
    for group in group_list:
        gen.reorder_children(group)

def set_remove_obj_btnCmd():
    selection_list = pm.ls(sl=True)
    object_set_list = []
    object_list = []

    for selection in selection_list:
        if selection.nodeType() == 'objectSet':
            object_set_list.append(selection)
        else:
            object_list.append(selection)

    if not object_set_list or not object_list:
        pm.warning('... Please select set(s) and object(s) in any order to continue')
    else:
        gen.remove_from_set(object_set_list, object_list)

def set_add_obj_btnCmd():
    list_selection = pm.ls(sl=True)
    list_object_set = []
    list_object = []

    for selection in list_selection:
        if selection.nodeType() == 'objectSet':
            list_object_set.append(selection)
        else:
            list_object.append(selection)

    if not list_object_set or not list_object:
        pm.warning('... Please select set(s) and object(s) in any order to continue')
    else:
        gen.add_to_set(list_object, list_object_set)

def create_button_fol_btnCmd():
    selection_list = pm.ls(sl=True)
    position_proxy_list = selection_list[:-1]
    mesh = selection_list[-1]

    for position_proxy in position_proxy_list:
        try :
            pm.select(position_proxy)
            cluster = pm.cluster()
            pos = pm.xform(cluster, q = True, ws = True, rp = True)
            pm.delete(cluster)
        except:
            pos = pm.xform(position_proxy, q = True, ws = True, rp = True)

        fol = gen.attach_fol_mesh(position_proxy.nodeName() + '_fol', mesh, pos)

def create_button_joint_btnCmd():

    selection_list = pm.ls(sl=True)
    position_proxy_list = selection_list[:-1]
    mesh = selection_list[-1]

    if not pm.objExists('button_grp'):
        global_button_grp = pm.group(em = True, n = 'button_grp')
        if pm.objExists('utils_grp'):
            utils_grp = pm.PyNode('utils_grp')
            pm.parent(global_button_grp, utils_grp)
            gen.lock_default_attr(global_button_grp)
    else:
        global_button_grp = pm.PyNode('button_grp')

    button_grp = pm.group(em = True, n = mesh.nodeName() + '_button_grp')
    gen.lock_hide_attr(button_grp)

    button_no_touch_grp = pm.group(em = True, n = mesh.nodeName() + '_no_touch_grp')
    gen.lock_hide_attr(button_no_touch_grp)
    button_no_touch_grp.v.set(0)

    button_controller_grp = pm.group(em = True, n = mesh.nodeName() + '_controller_grp')
    gen.lock_hide_attr(button_controller_grp)

    button_joint_grp = pm.group(em = True, n = mesh.nodeName() + '_joint_grp')
    gen.lock_hide_attr(button_joint_grp)

    pm.parent(button_grp, global_button_grp)
    pm.parent(button_no_touch_grp, button_controller_grp, button_joint_grp, button_grp)

    controller_scale = 10.00
    # if pm.objExists('INPUT_ANIM_GRP'):
    #     INPUT_ANIM_GRP = pm.PyNode('INPUT_ANIM_GRP')
    #     space_scale_ref = INPUT_ANIM_GRP.listRelatives(ad = True, type = 'mesh')
    #     controller_scale = gen.space_scale_to_ctrl_scale(space_scale_ref)

    counter = 1

    for position_proxy in position_proxy_list:
        button_name = 'button' + str(counter)

        try :
            pm.select(position_proxy)
            cluster = pm.cluster()
            pos = pm.xform(cluster, q = True, ws = True, rp = True)
            pm.delete(cluster)
        except:
            pos = pm.xform(position_proxy, q = True, ws = True, rp = True)

        fol = gen.attach_fol_mesh(mesh.nodeName() + '_' + button_name + '_fol', mesh, pos)
        pm.parent(fol, button_no_touch_grp)

        controller_grp = pm.group(em = True, name = mesh.nodeName() + '_' + button_name + '_ctrl_grp')
        controller = gen.controller_create('sphere', name= mesh.nodeName() + '_' + button_name + '_ctrl', color = 'red', scale = controller_scale)
        gen.freeze_transform(controller)
        gen.delete_history(controller)
        pm.parent(controller, controller_grp)
        pm.parent(controller_grp, button_controller_grp)
        pm.parentConstraint(fol, controller_grp, mo = False, skipTranslate = 'none', skipRotate = 'none')
        gen.lock_default_attr(controller_grp)

        gen.lock_hide_attr(controller, ['s'])
        joint = pm.createNode('joint', n = mesh.nodeName() + '_' + button_name + '_jnt')
        pm.parent(joint, button_joint_grp)
        pm.parentConstraint(controller, joint, mo = False, skipTranslate = 'none', skipRotate = 'none')
        gen.lock_default_attr(joint)

        counter += 1

def unlock_normal_btnCmd():
    selection_list = pm.ls(sl = True)
    for selection in selection_list:
        try:
            gen.unlock_normal(selection)
        except:
            pm.warning('{selection} is not compatiable, please contact Weerapot'.format(selection = selection.nodeName()))

def rename_tweak_btnCmd():
    gen.rename_tweak()

def clean_duplicate_btnCmd():
    selection_list = pm.ls(sl = True)
    for selection in selection_list:
        gen.clean_duplicate(selection)

def pipeline_sub_div_fix_btnCmd():
    import pymel.core as pm
    for mesh in pm.ls(sl=True):
        mesh.aiSubdivType.set(1)
        mesh.aiSubdivIterations.set(2)

def reset_vertex_local_translate_btnCmd():
    pm.polyMoveVertex(localTranslate = (0, 0, 0))
