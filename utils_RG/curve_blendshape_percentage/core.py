################################################################################
__Script__  = 'utils_RG.curve_blendshape_percentage.core'
__Author__  = 'Weerapot Chaoman'
__Version__ = 2.10
__Date__    = 20200510
################################################################################
import os, sys, subprocess, webbrowser, re, inspect
import pymel.core as pm
import maya.OpenMayaUI as mui
from collections import OrderedDict
################################################################################
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
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
try:
    from global_RG.Qt import Qt, QtCore, QtGui, QtWidgets, QtCompat
except:
    cmd = 'from '
    if __project__ in __self_path__:
        cmd += __project__ + '.'
    cmd += 'global_RG.Qt'
    cmd += ' import Qt, QtCore, QtGui, QtWidgets, QtCompat'
    exec(cmd)
################################################################################

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class PctBlendshape(general.General):

    def __init__(self):
        super(PctBlendshape, self).__init__()

    def apply_pct_bs_btnCmd(self):

        pm.undoInfo(openChunk = True)

        bs_dir = self.bs_dir_comboBox.currentText()
        bs_method = self.bs_method_comboBox.currentText()

        selection_list = pm.ls(sl = True)

        if selection_list:
            if len(selection_list) != 2: # invalid selection
                if len(selection_list) > 2:
                    pm.warning('... More than 2 obj(s) were selected, operation was not initiated.')
                else:
                    pm.warning('... Less than 2 obj(s) were selected, operation was not initiated')

            else: # continue

                driver_tfm = selection_list[0]
                driven_tfm = selection_list[1]

                driver_name = driver_tfm.stripNamespace()

                driver_crv_shape_list = pm.listRelatives(driver_tfm, ad = True, type = 'nurbsCurve')
                driver_crv_list = list(set(pm.listRelatives(driver_crv_shape_list, parent = True)))

                driven_crv_shp_list = pm.listRelatives(driven_tfm, ad = True, type = 'nurbsCurve')
                driven_crv_list = list(set(pm.listRelatives(driven_crv_shp_list, parent = True)))

                crv_length_list = []
                for crv in driver_crv_list:
                    crv_length_list.append(pm.arclen(crv))
                crv_length_list.sort()
                longest_val = crv_length_list[-1]

                if bs_method == 'Name Order':

                    driver_crv_list = self.natural_sort(driver_crv_list)
                    driven_crv_list = self.natural_sort(driven_crv_list)

                elif bs_method == 'Root Distance':

                    driver_crv_pos_info_list = []
                    for crv in driver_crv_list:
                        crv_shape = self.get_visible_shape(crv)
                        pm.select(crv_shape.nodeName() + '.cv[0]')
                        cluster = pm.cluster()
                        cluster_pos = pm.xform(cluster, q = True, ws = True, rp = True)
                        pm.delete(cluster)
                        driver_crv_pos_info_list.append([cluster_pos, crv])
                    driver_crv_pos_info_list.sort()

                    driver_crv_list = [] # rearrange/reorganise driver_crv_list
                    for crv in driven_crv_list:
                        crv_shape = self.get_visible_shape(crv)
                        pm.select(crv_shape.nodeName() + '.cv[0]')
                        cluster = pm.cluster()
                        cluster_pos = pm.xform(cluster, q = True, ws = True, rp = True)
                        pm.delete(cluster)

                        proximity_list = []
                        for pos_info in driver_crv_pos_info_list:
                            distance = self.get_distance(pos_info[0], cluster_pos)
                            proximity_list.append([distance, pos_info[1]])
                        proximity_list.sort()
                        closest_crv = proximity_list[0][1]
                        driver_crv_list.append(closest_crv)

                if not driven_tfm.hasAttr('_pct_bsn_'):
                    pm.addAttr(driven_tfm, ln = '_pct_bsn_', at = 'double', k = True)
                    driven_tfm._pct_bsn_.lock()

                if not driven_tfm.hasAttr('pct_bsn_src'):
                    pm.addAttr(driven_tfm, ln = 'pct_bsn_src', dataType = 'string', keyable = True)
                driven_tfm.pct_bsn_src.unlock()
                driven_tfm.pct_bsn_src.set(driver_tfm.fullPath())
                driven_tfm.pct_bsn_src.lock()

                if not driven_tfm.hasAttr('pct_bsn_en'):
                    pm.addAttr(driven_tfm, ln = 'pct_bsn_en', at = 'double', k = True, min = 0, max = 1, dv = 1)

                # blendshape, then set the weight
                for driver, driven in zip(driver_crv_list, driven_crv_list):

                    bs_name = driver.stripNamespace() + '_pct_bsn'

                    pct_val = 1 / longest_val * pm.arclen(driver)

                    if bs_dir == 'Normal':
                        pct_val = 1 - pct_val
                    elif bs_dir == 'Reverse':
                        pass

                    if pm.objExists(bs_name):
                        bs = pm.PyNode(bs_name)
                        pm.blendShape(bs, e = True, weight = [0, pct_val])
                    else:
                        bs = pm.blendShape(driver, driven, origin = 'world', weight = [0, pct_val], n = bs_name, envelope = 1)[0]

                    if not pm.isConnected(driven_tfm.pct_bsn_en, bs.en):
                        driven_tfm.pct_bsn_en >> bs.en

        pm.undoInfo(closeChunk = True)

    def delete_pct_bs_btnCmd(self):

        pm.undoInfo(openChunk = True)

        selection_list = pm.ls(sl = True)

        bs_list = []
        src_list = []

        for selection in selection_list:
            if selection.hasAttr('pct_bsn_en'):
                bs_list = pm.listConnections(selection.pct_bsn_en)
                src_list.append(selection)
            else:
                nrb_crv_shp_list = pm.listRelatives(selection, ad = True, type = 'nurbsCurve')
                bs_list = pm.listConnections(nrb_crv_shp_list, type = 'blendShape')
                bs_list = list(set(bs_list))
                if bs_list:
                    src_list = []
                    for bs in bs_list:
                        if '_pct_bsn' not in bs.nodeName():
                            bs_list.remove(bs)
                        else:
                            src_list.extend(pm.listConnections(bs.envelope))
                    src_list = list(set(src_list))

        if src_list:
            for src in src_list:
                for attr in ['_pct_bsn_', 'pct_bsn_src', 'pct_bsn_en']:
                    if src.hasAttr(attr):
                        exec('src.{0}.unlock()'.format(attr))
                        exec('pm.deleteAttr(src.{0})'.format(attr))
            pm.delete(bs_list)

        pm.undoInfo(closeChunk = True)

class Gui(QtWidgets.QWidget, ui.UI, PctBlendshape):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(Gui, self).__init__(parent)

        self._ui            = 'ui_hair_percentage_blendshape'
        self._width         = 250.00
        self._height        = 15.00
        self._title_name    = 'Hair % BlendShape'
        self._title         = '{title_name} v{version}'.format(title_name = self._title_name, version = __Version__)

        self.delete_UI(self._ui)

        self.setObjectName(self._ui)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True) # destroy this widget when close
        self.resize(self._width, self._height)
        self.setWindowTitle(self._title)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.NonModal)

        self.gui_init()

    def gui_init(self):

        self.main_layout = self.create_QVBoxLayout(parent = self)

        self.user_input_layout = self.create_QGridLayout(parent = self.main_layout, w = self._width, nc = 2)

        self.bs_dir_label = self.create_QLabel(text = 'Blendshape Weight Direction', parent = self.user_input_layout, co = (0, 0))
        self.bs_dir_label.setAlignment(QtCore.Qt.AlignCenter)
        bs_dir_list = ['Normal', 'Reverse']
        self.bs_dir_comboBox = self.create_QComboBox(item_list = bs_dir_list, parent = self.user_input_layout, co = (0, 1))

        self.bs_method_label = self.create_QLabel(text = 'Blendshape Method', parent = self.user_input_layout, co = (1, 0))
        self.bs_method_label.setAlignment(QtCore.Qt.AlignCenter)
        bs_method_list = ['Name Order', 'Root Distance']
        self.bs_method_comboBox = self.create_QComboBox(item_list = bs_method_list, parent = self.user_input_layout, co = (1, 1))

        self.button_layout = self.create_QGridLayout(parent = self.main_layout, w = self._width, nc = 2)
        self.apply_button = self.create_QPushButton(text = 'Apply', parent = self.button_layout, co = (0, 0), c = self.apply_pct_bs_btnCmd)
        self.apply_button = self.create_QPushButton(text = 'Delete', parent = self.button_layout, co = (0, 1), c = self.delete_pct_bs_btnCmd)

        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)

def run(*args, **kwargs):
    gui = Gui()
    gui.show()
