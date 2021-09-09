################################################################################
__Script__      = 'utils_RG.average_vertex_util.core'
__Author__      = 'Weerapot Chaoman'
__Version__     = 3.50
__Date__        = 2021
################################################################################
import os, sys, subprocess, webbrowser, re, inspect, importlib
import pymel.core as pm
import pymel.all as pall
import maya.OpenMayaUI as mui
from collections import OrderedDict
from random import shuffle
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
    cmd += 'importlib.reload(' + as_name + ');'
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

class AverageVertexUtil(general.General):

    def __init__(self):
        super(AverageVertexUtil, self).__init__()

av = AverageVertexUtil()

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class Gui(QtWidgets.QWidget, ui.UI):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(Gui, self).__init__(parent, *args, **kwargs)

        self._ui            = 'ui_average_vertex_util'
        self._width         = 600.00
        self._height        = 400.00
        self._title_name    = 'Average Vertex Util'
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

        self.grid_layout = self.create_QGridLayout(parent = self.main_layout, w = self._width, nc = 2, cwp = (3, 2))

        # PAV
        self.main_tab_widget = self.create_QTabWidget(parent = self.grid_layout, co = (0, 0))
        # Button
        self.button_layout = self.create_QVBoxLayout(parent = self.grid_layout, co = (0, 1))

        self.reload_btn = self.create_QPushButton(text = 'Load Selected Meshes', parent = self.button_layout, c = self.main_tab_widget_update)
        self.refresh_btn = self.create_QPushButton(text = 'Refresh', parent = self.button_layout, c = self.refresh_btnCmd)

        self.separatorA = self.create_separator(parent = self.button_layout)

        self.delete_pav_btn = self.create_QPushButton(text = 'Delete Selected PAV Nodes')

        self.delete_btn = self.create_QPushButton(text = 'Delete Selected PAV', parent = self.button_layout, c = self.delete_selected_pav_btnCmd)
        self.undo_redo_layout = self.create_QGridLayout(parent = self.button_layout, w = self._width / 5 * 2, nc = 2)
        self.undo_btn = self.create_QPushButton(text = 'Undo', parent = self.undo_redo_layout, co = (0, 0), c = self.undo_btnCmd)
        self.undo_btn = self.create_QPushButton(text = 'Redo', parent = self.undo_redo_layout, co = (0, 1), c = self.redo_btnCmd)

        self.separatorB = self.create_separator(parent = self.button_layout)

        self.PAV_attr_layout = self.create_QGridLayout(parent = self.button_layout, w = self._width / 5 * 2, nc = 2)
        self.create_PAV_attr_btn = self.create_QPushButton(text = 'Create PAV Attribute', parent = self.PAV_attr_layout, c = self.create_PAV_attr_btnCmd)
        self.delete_PAV_attr_btn = self.create_QPushButton(text = 'Delete PAV Attribute', parent = self.PAV_attr_layout, c = self.delete_PAV_attr_btnCmd)

        self.button_layout.setAlignment(QtCore.Qt.AlignTop)

        self.main_tab_widget_update()

    def create_pav_tab(self, target=None):

        target = pm.PyNode(target)
        target_full_path = target.fullPath()

        # tab_widget = self.create_QWidget(parent = self.main_tab_widget)
        tab_widget = self.create_QWidget()
        self.main_tab_widget.addTab(tab_widget, target.stripNamespace())
        tab_layout = self.create_QGridLayout(parent = tab_widget, h = self._height, nr = 2, rhp = (1, 9))

        path_line_edit = self.create_QLineEdit(text = target_full_path, read_only = True, parent = tab_layout, co = (0, 0))

        pav_list_widget = self.create_QListWidget(parent = tab_layout, co = (1, 0), ams = True)
        pav_list = av.get_average_vertex(target)
        pav_list = av.natural_sort(pav_list)
        for pav in pav_list:
            pav_list_widget.addItem(pav.nodeName())

    def refresh_btnCmd(self):

        pm.undoInfo(openChunk = True)

        tab_layout_list = self.main_tab_widget.findChildren(QtWidgets.QGridLayout)

        for tab_layout in tab_layout_list:

            line_edit = tab_layout.itemAtPosition(0, 0).widget()
            mesh = line_edit.text()
            mesh = pm.PyNode(mesh)

            list_widget = tab_layout.itemAtPosition(1, 0).widget()
            list_widget.clear()

            pav_list = av.get_average_vertex(mesh)
            pav_list = av.natural_sort(pav_list)
            for pav in pav_list:
                list_widget.addItem(pav.nodeName())

        pm.undoInfo(closeChunk = True)

    def main_tab_widget_update(self):
        selection_list = pm.ls(sl = True)
        selection_dict = {}

        self.main_tab_widget.clear()
        # self.clear_QWidget(self.main_tab_widget)

        for selection in selection_list:
            print(selection)
            self.create_pav_tab(selection)

    def get_selected_items(self):
        # return [mesh, selected_pav_list]
        if self.main_tab_widget.currentWidget():

            active_tab = self.main_tab_widget.currentWidget()

            line_edit = self.main_tab_widget.findChild(QtWidgets.QLineEdit)
            mesh = pm.PyNode(line_edit.text())

            list_widget = self.main_tab_widget.findChild(QtWidgets.QListWidget)
            selected_text_list = list_widget.selectedItems()
            selected_pav_list = []
            for text in selected_text_list:
                selected_pav_list.append(pm.PyNode(text.text()))
            selected_pav_list = av.natural_sort(selected_pav_list)

            return(mesh, selected_pav_list)

    def undo_btnCmd(self):
        pm.undo()
        self.refresh_btnCmd()

    def redo_btnCmd(self):
        pm.redo()
        self.refresh_btnCmd()

    def delete_selected_pav_btnCmd(self):
        pm.undoInfo(openChunk = True)
        selected_pav_list = self.get_selected_items()[1]
        pm.delete(selected_pav_list)
        self.refresh_btnCmd()
        pm.undoInfo(closeChunk = True)

    def create_PAV_attr_btnCmd(self):

        pm.undoInfo(openChunk = True)

        selected_item_info = self.get_selected_items()
        mesh = selected_item_info[0]
        selected_pav_list = selected_item_info[1]

        current_frame = pm.currentTime(query = True)
        current_frame = int(current_frame)

        # Attributes
        if not pm.attributeQuery('average_vtx_global', node = mesh, exists = True):
            mesh.addAttr('average_vtx_global', keyable = True, attributeType = 'float', max = 1, min = 0, dv = 1)
        global_amp_attr = mesh.average_vtx_global

        name_sub_amp_attr = 'f{0}_'.format(current_frame)
        index = av.get_attribute_increment(mesh, name_sub_amp_attr)
        name_sub_amp_attr += str(index)

        mesh.addAttr(name_sub_amp_attr, keyable = True, attributeType = 'float', max = 10, min = 0, dv = 10)
        sub_amp_attr = getattr(mesh, name_sub_amp_attr)
        
        name_amp = av.compose_snake_case(mesh.stripNamespace() + '_' + name_sub_amp_attr + '_mdv')
        if not pm.objExists(name_amp):
            amp = pm.createNode('multiplyDivide', name = name_amp)
            amp.operation.set(1)
        else:
            amp = pm.PyNode(name_amp)

        sub_amp_attr >> amp.i1x
        for axis in ['x', 'y', 'z']:
            pm.connectAttr(global_amp_attr, '{0}.i2{1}'.format(amp, axis))

        for pav in selected_pav_list:
            pav.iterations.disconnect()
            pm.connectAttr(amp.ox, pav.iterations)
            increment = self.pav_name_increment(name_sub_amp_attr)
            pav.rename('{0}_{1}_pav'.format(name_sub_amp_attr, increment))

        self.refresh_btnCmd()
        pm.select(mesh)

        pm.undoInfo(closeChunk = True)

    def pav_name_increment(self, input_str):

        matching_pav_list = pm.ls('*{0}*'.format(input_str), type = 'polyAverageVertex')

        if matching_pav_list:

            matching_pav_list = av.natural_sort(matching_pav_list)

            latest_increment = matching_pav_list[-1]
            latest_increment = re.findall(r'[0-9]+_pav', str(latest_increment))[0]
            latest_increment = re.findall(r'[0-9]+', latest_increment)[0]
            new_increment = int(latest_increment)
            new_increment += 1
        else:
            new_increment = 1
        return(new_increment)

    def delete_PAV_attr_btnCmd(self):

        pm.undoInfo(openChunk = True)

        selection = pm.ls(sl = True)[0]
        selected_attr_list = av.get_selected_attributes()

        global_amp_attr = pm.PyNode(selection.nodeName() + '.average_vtx_global')

        if global_amp_attr in selected_attr_list:
            selected_attr_list.remove(global_amp_attr)
            selected_attr_list.append(global_amp_attr)

        for attr in selected_attr_list:
            if attr == global_amp_attr:
                if not pm.listConnections(attr):
                    pm.deleteAttr(attr)
            else:
                mdv_list = pm.listConnections(attr, type = 'multiplyDivide')
                if mdv_list:
                    sample_mdv = mdv_list[0]
                    if pm.isConnected(global_amp_attr, sample_mdv.i2x): # check if the selected attribute is really the tool's attr
                        for mdv in mdv_list:
                            pav_list = mdv.listConnections(type = 'polyAverageVertex')
                            pav_list = av.natural_sort(pav_list)
                            for pav in pav_list:
                                pav.rename('polyAverageVertex1')
                        pm.delete(mdv_list)
                        pm.deleteAttr(attr)

        self.refresh_btnCmd()

        pm.undoInfo(closeChunk = True)

    def test_btnCmd(self):
        print(self.get_selected_items())

def run():
    gui = Gui()
    gui.show()
