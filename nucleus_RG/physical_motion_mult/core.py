################################################################################
__Script__	= 'nucleus_SP.physical_motion_mult.core'
__Author__	= 'Weerapot Chaoman'
__Version__	= 5.0
__Date__	= 20200504
################################################################################
import os, subprocess, webbrowser, sys, re, inspect
import pymel.core as pm
import maya.OpenMayaUI as mui
from collections import OrderedDict
################################################################################
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
try:
    from global_SP.Qt import Qt, QtCore, QtGui, QtWidgets, QtCompat
except:
    cmd = 'from '
    if __project__ in __self_path__:
        cmd += __project__ + '.'
    cmd += 'global_RG.Qt'
    cmd += ' import Qt, QtCore, QtGui, QtWidgets, QtCompat'
    exec(cmd)
################################################################################
module_list = []
module_list.append(['global_RG.general', 'core', 'general'])
module_list.append(['global_RG.ui', 'core', 'ui'])
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
plugin_list = ['AbcExport.mll', 'AbcImport.mll', 'matrixNodes.mll']
for plugin in plugin_list:
    if not pm.pluginInfo(plugin, q = True, loaded = True):
        pm.loadPlugin(plugin)
################################################################################

class OnTheFly(object): # test area
    def __init__(self):
        super(OnTheFly, self).__init__()

    def compare_transposeMatrix_worldInverseMatrix(self):
        driver_tfm = pm.group(em = True, n = 'driver_tfm')
        driven_tpm_tfm = pm.group(em = True, n = 'driven_tpm_tfm')
        driven_ivm_tfm = pm.group(em = True, n = 'driven_ivm_tfm')

        tmn_transposeMatrix_node = pm.createNode('transposeMatrix')
        tmn_decomposeMatrix_node = pm.createNode('decomposeMatrix')

        driver_tfm.matrix >> tmn_transposeMatrix_node.inputMatrix
        tmn_transposeMatrix_node.outputMatrix >> tmn_decomposeMatrix_node.inputMatrix
        tmn_decomposeMatrix_node.outputRotate >> driven_tpm_tfm.r

        ivm_decomposeMatrix_node = pm.createNode('decomposeMatrix')
        driver_tfm.worldInverseMatrix >> ivm_decomposeMatrix_node.inputMatrix
        ivm_decomposeMatrix_node.outputRotate >> driven_ivm_tfm.r

    def add_remove(self):
        selection = pm.ls(sl = True)
        pm.sets('cluster1Set', fe = selection)
        pm.sets('cluster1Set', remove = selection)

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

gen = general.General()

class GUI(ui.UI, QtWidgets.QWidget):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(GUI, self).__init__(parent)

        self._ui = 'physical_motion_mult_ui'
        self._width = 300.00
        self._height = 100.00
        self._version = __Version__
        self._title_name = 'Physical Motion Mult'
        self._title = '{titleName} v{version}'.format(titleName=self._title_name, version=self._version)

        self.delete_UI(self._ui)

        self.setObjectName(self._ui)
        self.resize(self._width, self._height)
        self.setWindowTitle(self._title)
        self.setWindowFlags(QtCore.Qt.Window)

        self.main_QVBoxLayout = self.create_QVBoxLayout(parent = self)
        self.gui_init()

    def gui_init(self):

        bake_QGridLayout = self.create_QGridLayout(parent = self.main_QVBoxLayout)
        bake_step_floatField = self.create_floatField(label = 'Step', precision = 2, parent = bake_QGridLayout, co = (0, 0))
        bake_QPushButton = self.create_QPushButton(text = 'Bake', parent = bake_QGridLayout, co = (0, 1), cmd = self.bake_btnCmd)
        self.bake_step_floatField = bake_step_floatField

        self.create_separator(parent = self.main_QVBoxLayout)

        connect_motionMult_QPushButton = self.create_QPushButton(
            text = 'Connect Motion Mult', parent = self.main_QVBoxLayout, cmd = self.connect_mm_btnCmd,
            )

        self.create_separator(parent = self.main_QVBoxLayout)

        input_cluster_QVBoxLayout = self.create_QVBoxLayout(parent = self.main_QVBoxLayout)
        input_cluster_QLabel = self.create_QLabel(text = 'input_cluster', parent = input_cluster_QVBoxLayout)
        input_cluster_QLabel.setAlignment(QtCore.Qt.AlignCenter)
        input_cluster_buttons_QGridLayout = self.create_QGridLayout(parent = input_cluster_QVBoxLayout)
        input_cluster_add_QPushButton = self.create_QPushButton(
            text = 'Add', parent = input_cluster_buttons_QGridLayout, co = (0, 0), cmd = self.input_cluster_add_btnCmd,
            )
        input_cluster_remove_QPushButton = self.create_QPushButton(
            text = 'Remove', parent = input_cluster_buttons_QGridLayout, co = (0, 1), cmd = self.input_cluster_remove_btnCmd,
            )

        self.create_separator(parent = self.main_QVBoxLayout)

        output_cluster_QVBoxLayout = self.create_QVBoxLayout(parent = self.main_QVBoxLayout)
        output_cluster_QLabel = self.create_QLabel(text = 'output_cluster', parent = output_cluster_QVBoxLayout)
        output_cluster_QLabel.setAlignment(QtCore.Qt.AlignCenter)
        output_cluster_buttons_QGridLayout = self.create_QGridLayout(parent = output_cluster_QVBoxLayout)
        output_cluster_add_QPushButton = self.create_QPushButton(
            text = 'Add', parent = output_cluster_buttons_QGridLayout, co = (0, 0), cmd = self.output_cluster_add_btnCmd)
        output_cluster_remove_QPushButton = self.create_QPushButton(
            text = 'Remove', parent = output_cluster_buttons_QGridLayout, co = (0, 1), cmd = self.output_cluster_remove_btnCmd)

class PhysicalMotionMult(GUI):

    def __init__(self):

        super(PhysicalMotionMult, self).__init__()

        self.name_utils_grp = 'mm_utils_grp'

        self.name_main_ctrl = 'mm_main_ctrl'
        self.name_offset_ctrl = 'mm_offset_ctrl'

        self.name_input_grp = 'mm_input_grp'
        self.name_input_tfm = 'mm_input_tfm'
        self.name_input_tfm_decomposeMatrix = 'mm_input_tfm_decomposeMatrix'
        self.name_inputStatic_tfm = 'mm_inputStatic_tfm'
        self.name_staticRef_tfm_decomposeMatrix = 'mm_staticRef_tfm_decomposeMatrix'

        self.name_bwd_multMatrix = 'mm_bwd_multMatrix'
        self.name_bwd_decomposeMatrix = 'mm_bwd_decomposeMatrix'
        self.name_bwd_grp = 'mm_bwd_grp'

        self.name_fwd_multMatrix = 'mm_fwd_multMatrix'
        self.name_fwd_decomposeMatrix = 'mm_fwd_decomposeMatrix'
        self.name_fwd_grp = 'mm_fwd_grp'

        self.name_amplifier = 'mm_amplifier'

        self.name_input_cluster = 'mm_input_cluster'
        self.name_output_cluster = 'mm_output_cluster'

    def bake_btnCmd(self):

        selection_list = pm.ls(sl = True)

        nucleus_list = pm.ls(type = 'nucleus')
        nucleus_current_setting_list = []
        for nucleus in nucleus_list:
            current_setting = nucleus.enable.get()
            nucleus_current_setting_list.append([nucleus, current_setting])
            nucleus.enable.set(0)

        step = float(self.bake_step_floatField.text())

        attr_list = []
        for attr in ['t', 'r']:
            for axis in ['x', 'y', 'z']:
                attr_list.append(attr + axis)

        start_frame = pm.playbackOptions(q = True, min = True)
        start_frame -= 30
        end_frame = pm.playbackOptions(q = True, max = True)
        end_frame += 10

        pm.bakeResults(selection_list, at = attr_list, t = (start_frame, end_frame), sb = step, simulation = True, minimizeRotation = True)

        for nucleus in nucleus_current_setting_list:
            nucleus[0].enable.set(nucleus[1])

        # check if rivet:
        for selection in selection_list:
            psi = selection.listConnections(type = 'pointOnSurfaceInfo')
            if psi:
                aimCon = selection.listRelatives(type = 'aimConstraint')
                if aimCon:
                    loft = pm.listConnections(psi, type = 'loft')
                    if loft:
                        cfme = pm.listConnections(loft, type = 'curveFromMeshEdge')
                        if cfme:
                            pm.delete(psi, aimCon, loft, cfme)

    def cluster_get_objectSet(self, cluster_tfm):
        cluster_tfm = pm.PyNode(cluster_tfm)
        cluster = cluster_tfm.listConnections(type = 'cluster')
        cluster_objectSet = pm.listConnections(cluster, type = 'objectSet')
        print cluster_objectSet

    def cluster_edit(self, cluster_name=None, object_list=None, mode='add'):
        # mode: 'add', 'remove'

        target_list = None
        if object_list:
            target_list = []
            mesh_list = pm.listRelatives(object_list, ad = True, type = 'mesh')
            curve_list = pm.listRelatives(object_list, ad = True, type  = 'nurbsCurve')
            target_list.extend(mesh_list)
            target_list.extend(curve_list)
            if not target_list:
                target_list = object_list

        if not pm.objExists(cluster_name):
            pm.select(cl = True)
            cluster = pm.cluster()
            cluster[1].rename(cluster_name)
            cluster = pm.PyNode(cluster_name)
        else:
            cluster = pm.PyNode(cluster_name)

        cluster_cluster = cluster.listConnections(type = 'cluster')
        cluster_objectSet = pm.listConnections(cluster_cluster, type = 'objectSet')[0]

        if mode == 'add':
            pm.sets(cluster_objectSet, fe = object_list)
        elif mode == 'remove':
            pm.sets(cluster_objectSet, remove = object_list)

    def input_cluster_add_btnCmd(self):
        selection_list = pm.ls(sl = True)
        self.cluster_edit(cluster_name = self.name_input_cluster, object_list = selection_list, mode = 'add')

    def input_cluster_remove_btnCmd(self):
        selection_list = pm.ls(sl = True)
        self.cluster_edit(cluster_name = self.name_input_cluster, object_list = selection_list, mode = 'remove')

    def output_cluster_add_btnCmd(self):
        selection_list = pm.ls(sl = True)
        self.cluster_edit(cluster_name = self.name_output_cluster, object_list = selection_list, mode = 'add')

    def output_cluster_remove_btnCmd(self):
        selection_list = pm.ls(sl = True)
        self.cluster_edit(cluster_name = self.name_output_cluster, object_list = selection_list, mode = 'remove')

    def create_mm_controller(self, scale=1.0):
        # main_ctrl
        if not pm.objExists(self.name_main_ctrl):
            main_ctrl = gen.controller_create(
                type = 'four_directional_arrow', name = self.name_main_ctrl, color = 'light_blue', scale = scale,
                )
            gen.lock_hide_attr(main_ctrl, ['s'])
            pm.addAttr(main_ctrl, ln = '__motion_mult__', at = 'double', keyable = True)
            main_ctrl.__motion_mult__.lock()
            for attr in ['t', 'r']:
                for axis in ['x', 'y', 'z']:
                    pm.addAttr(main_ctrl, ln = 'mm_{attr}{axis}'.format(attr = attr, axis = axis), at = 'double', keyable = True, dv = 1)
            pm.addAttr(main_ctrl, ln = 'offset_ctrl', at = 'bool', keyable = True, dv = True)
            # main_ctrl_zro_grp
            main_ctrl_zro_grp = pm.group(em = True, w = True, n = self.name_main_ctrl + '_zro_grp')
            pm.parent(main_ctrl, main_ctrl_zro_grp)
        else:
            main_ctrl = pm.PyNode(self.name_main_ctrl)
            main_ctrl_zro_grp = pm.PyNode(self.name_main_ctrl + '_zro_grp')

        # offset_ctrl
        if not pm.objExists(self.name_offset_ctrl):
            offset_ctrl = gen.controller_create(
                type = 'offset', name = 'offset_ctrl', color = 'white', scale = scale,
                )
            gen.lock_hide_attr(offset_ctrl, ['s', 'v'])
            # connect to main_ctrl.ofset_ctrl
            offset_ctrl_shape = gen.get_visible_shape(offset_ctrl)
            main_ctrl.offset_ctrl >> offset_ctrl_shape.v
            # offset_ctrl_zro_grp
            offset_ctrl_zro_grp = pm.group(em = True, w = True, n = self.name_offset_ctrl + '_zro_grp')
            pm.parent(offset_ctrl, offset_ctrl_zro_grp)
            pm.parent(offset_ctrl_zro_grp, main_ctrl)
            # lock zero group default attr
            gen.lock_default_attr(offset_ctrl_zro_grp)
        else:
            offset_ctrl = pm.PyNode(self.name_offset_ctrl)
            offset_ctrl_zro_grp = pm.PyNode(self.name_offset_ctrl + '_zro_grp')

        return(main_ctrl, main_ctrl_zro_grp, offset_ctrl, offset_ctrl_zro_grp)

    def connect_mm_btnCmd(self):

        selection_list = pm.ls(sl = True)

        if selection_list:

            if len(selection_list) > 1:
                pm.warning('... more than 1 object are being selected, mm will be apply on the first order of selection')
            selection = selection_list[0]
            input_tfm, staticRef_tfm = self.create_mm_network()

            # duplicate mm_input_tfm, then transfer output connections
            output_connection_list = input_tfm.listConnections(
                skipConversionNodes = True, source = False, destination = True, connections = True, plugs = True,
                )
                # input_connection_list = pm.listConnections(selection, scn = True, s = True, d = False, c = True, p = True)
                # output_connection_list = pm.listConnections(selection, scn = True, s = False, d = True, c = True, p = True)

            input_tfm_dup = pm.duplicate(input_tfm)[0]
            pm.reorder(input_tfm_dup, front = True)

            for connection in output_connection_list:
                pm.connectAttr(input_tfm_dup.nodeName() + '.' + connection[0].attrName(), connection[1], force = True)

            pm.delete(input_tfm)
            input_tfm_dup.rename(self.name_input_tfm)

            # connect to selection
            point_con = pm.pointConstraint(selection, input_tfm, mo = False, skip = 'none')
            pm.delete(point_con)
            pm.parentConstraint(selection, input_tfm, mo = True, skipTranslate = 'none', skipRotate = 'none')

            point_con = pm.pointConstraint(selection, staticRef_tfm, mo = False, skip = 'none')
            pm.delete(point_con)

    def create_mm_network(self):
        # return input tfm << connect transform here

        if not pm.objExists(self.name_input_tfm):

            ctrl_scale = 1.00

            utils_grp = pm.group(em = True, n = self.name_utils_grp)
            gen.lock_default_attr(utils_grp)

            main_ctrl, main_ctrl_zro_grp, offset_ctrl, offset_ctrl_zro_grp = self.create_mm_controller(scale = ctrl_scale)

            input_grp = pm.group(em = True, w = True, n = self.name_input_grp)
            gen.outliner_color_apply(input_grp, color = 'green')
            gen.lock_default_attr(input_grp)
            input_tfm = pm.group(em = True, parent = input_grp, n = self.name_input_tfm) # tfm receiving the animation
            gen.outliner_color_apply(input_tfm, color = 'pale_blue')
            staticRef_tfm = pm.group(em = True, parent = input_grp, n = self.name_inputStatic_tfm) # static tfm for value blending
            gen.outliner_color_apply(staticRef_tfm, color = 'pale_purple')

            # bwd
            bwd_multMatrix  = pm.createNode('multMatrix', n = self.name_bwd_multMatrix)
            input_tfm.worldInverseMatrix >> bwd_multMatrix.matrixIn[0]
            offset_ctrl.worldMatrix >> bwd_multMatrix.matrixIn[1]

            bwd_decomposeMatrix = pm.createNode('decomposeMatrix', n = self.name_bwd_decomposeMatrix)
            bwd_multMatrix.matrixSum >> bwd_decomposeMatrix.inputMatrix

            bwd_grp = pm.group(em = True, w = True, n = self.name_bwd_grp)
            bwd_decomposeMatrix.outputTranslate >> bwd_grp.t
            bwd_decomposeMatrix.outputRotate >> bwd_grp.r

            # fwd
            fwd_multMatrix = pm.createNode('multMatrix', n = self.name_fwd_multMatrix)
            bwd_grp.worldInverseMatrix >> fwd_multMatrix.matrixIn[0]
            # input_tfm.worldMatrix >> fwd_multMatrix.matrixIn[1]

            fwd_decomposeMatrix = pm.createNode('decomposeMatrix', n = self.name_fwd_decomposeMatrix)
            fwd_multMatrix.matrixSum >> fwd_decomposeMatrix.inputMatrix

            fwd_grp = pm.group(em = True, n = self.name_fwd_grp)
            fwd_decomposeMatrix.outputTranslate >> fwd_grp.t
            fwd_decomposeMatrix.outputRotate >> fwd_grp.r

            # ctrl
            input_tfm_decomposeMatrix = pm.createNode('decomposeMatrix', n = self.name_input_tfm_decomposeMatrix)
            input_tfm.worldMatrix >> input_tfm_decomposeMatrix.inputMatrix

            staticRef_tfm_decomposeMatrix = pm.createNode('decomposeMatrix', n = self.name_staticRef_tfm_decomposeMatrix)
            staticRef_tfm.worldMatrix >> staticRef_tfm_decomposeMatrix.inputMatrix

            for attr, attribute in zip(['t', 'r'], ['translate', 'rotate']):
                for axis, rgb in zip(['x', 'y', 'z'], ['r', 'g', 'b']):
                    blend_color = pm.createNode('blendColors', n = '{name_amplifier}_{attr}{axis}'.format(
                        name_amplifier = self.name_amplifier, attr = attr, axis = axis,
                        ))
                    pm.connectAttr(
                        '{main_ctrl}.mm_{attr}{axis}'.format(main_ctrl = main_ctrl.nodeName(), attr = attr, axis = axis),
                        '{blend_color}.blender'.format(blend_color = blend_color.nodeName()),
                        )
                    pm.connectAttr(
                        '{input_tfm_decomposeMatrix}.output{attribute}{axis}'.format(
                            input_tfm_decomposeMatrix = input_tfm_decomposeMatrix.nodeName(),
                            attribute = attribute.capitalize(), axis = axis.upper()),
                        '{blend_color}.c1{rgb}'.format(blend_color = blend_color.nodeName(), rgb = rgb),
                        )
                    pm.connectAttr(
                        '{staticRef_tfm_decomposeMatrix}.output{attribute}{axis}'.format(
                            staticRef_tfm_decomposeMatrix = staticRef_tfm_decomposeMatrix.nodeName(),
                            attribute = attribute.capitalize(), axis = axis.upper()),
                        '{blend_color}.c2{rgb}'.format(blend_color = blend_color.nodeName(), rgb = rgb),
                        )
                    pm.connectAttr(
                        '{blend_color}.output{rgb}'.format(blend_color = blend_color.nodeName(), rgb = rgb.upper()),
                        '{main_ctrl_zro_grp}.{attr}{axis}'.format(
                            main_ctrl_zro_grp = main_ctrl_zro_grp.nodeName(), attr = attr, axis = axis,
                        ))
            gen.lock_default_attr(main_ctrl_zro_grp)

            pm.select(cl = True) # just in case
            input_cluster = pm.cluster()
            input_cluster[1].rename(self.name_input_cluster)

            pm.select(cl = True) # just in case
            output_cluster = pm.cluster()
            output_cluster[1].rename(self.name_output_cluster)

            pm.parent(input_cluster, bwd_grp)
            pm.parent(output_cluster, fwd_grp)

            pm.parent(main_ctrl_zro_grp, input_grp, bwd_grp, fwd_grp, utils_grp)

        else:
            input_tfm = pm.PyNode(self.name_input_tfm)
            staticRef_tfm = pm.PyNode(self.name_inputStatic_tfm)

        return(input_tfm, staticRef_tfm)

def run():
    pmm = PhysicalMotionMult()
    pmm.show()
