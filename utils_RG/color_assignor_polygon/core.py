################################################################################
__Script__  = 'utils_RG.color_assignor_polygon.core'
__Author__  = 'Weerapot Chaoman'
__Version__	= 2.03
__Date__    = 20200507
################################################################################
import os, sys, subprocess, webbrowser, re, inspect
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

gen = general.General()

class ColorAssignorPolygon(object):

    def __init__(self, *args, **kwargs):
        super(ColorAssignorPolygon, self).__init__(*args, **kwargs)

    def assign_poly_shader_to_selection(self, color_name):
        transparency = self.transparency_slider.value()
        selection_list = pm.ls(sl = True)
        gen.assign_poly_shader(target_list = selection_list, color_name = color_name, transparency = transparency)
        pm.select(selection_list)

    def assign_randomize_poly_shader_to_selection(self):
        selection_list = pm.ls(sl = True)
        randomize_color_list = []

        transparency = self.transparency_slider.value()

        if self.randomize_normal_checkBox.checkState():
            for color in self.color_list:
                if 'light_' not in color:
                    randomize_color_list.append(color)

        if self.randomize_light_checkBox.checkState():
            for color in self.color_list:
                if 'light_' in color:
                    randomize_color_list.append(color)

        if self.randomize_skin_checkBox.checkState():
            randomize_color_list.extend(self.skin_color_list)

        if self.randomize_mono_checkBox.checkState():
            randomize_color_list.extend(self.mono_color_list)

        shuffle(randomize_color_list)

        regex = re.compile(r'body|skin', re.IGNORECASE)

        for i in range (0, len(selection_list)):
            print selection_list[i].nodeName()
            print regex.findall(selection_list[i].nodeName())
            if regex.findall(selection_list[i].nodeName()):
                gen.assign_poly_shader(target_list = selection_list[i], color_name = 'skin', transparency = transparency)
            else:
                gen.assign_poly_shader(target_list = selection_list[i], color_name = randomize_color_list[i%len(randomize_color_list)], transparency = transparency)

        pm.select(selection_list)

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class Gui(QtWidgets.QWidget, ColorAssignorPolygon, ui.UI):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(Gui, self).__init__(parent, *args, **kwargs)

        self.color_rgb_dict = gen.color_rgb_dict

        self._ui            = 'ui_color_assignor_polygon'
        self._width         = 350.00
        self._height        = 100.00
        self._title_name    = 'Polygon Color Assignor'
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

        self.transparency_label = self.create_QLabel(text = 'Transparency')
        self.transparency_slider = self.create_QHSlider(min = 0, max = 100, val = 100)
        self.transparency_spinBox = self.create_QSpinBox(range = (0, 100), val = 100)
        self.transparency_slider.valueChanged.connect(self.transparency_slider_cc)
        self.transparency_spinBox.valueChanged.connect(self.transparency_spinBox_cc)

        self.color_grid_layout = self.create_QGridLayout(w = self._width, nc = 2, parent = self.main_layout)
        self.color_list = []
        self.color_list.extend(['blue', 'light_blue'])
        self.color_list.extend(['sea_green', 'light_sea_green'])
        self.color_list.extend(['green', 'light_green'])
        self.color_list.extend(['yellow', 'light_yellow'])
        self.color_list.extend(['orange', 'light_orange'])
        self.color_list.extend(['red', 'light_red'])
        self.color_list.extend(['brown', 'light_brown'])
        self.color_list.extend(['purple', 'light_purple'])
        self.color_list.extend(['pink', 'light_pink'])
        color_button_list = []
        for color in self.color_list:
            button = self.create_QPushButton(text = gen.compose_nice_name(color), bgc = self.color_rgb_dict[color],
                c = pall.Callback(self.assign_poly_shader_to_selection, color))
            color_button_list.append(button)
        self.parent_QGridLayout(parent = self.color_grid_layout, child_list = color_button_list, max_column = 2)

        self.skin_grid_layout = self.create_QGridLayout(w = self._width, nc = 3, parent = self.main_layout)
        self.skin_color_list = ['skin', 'skin_light', 'skin_dark']
        skin_color_button_list = []
        for color in self.skin_color_list:
            button = self.create_QPushButton(text = gen.compose_nice_name(color), bgc = self.color_rgb_dict[color],
                c = pall.Callback(self.assign_poly_shader_to_selection, color))
            skin_color_button_list.append(button)
        self.parent_QGridLayout(parent = self.skin_grid_layout, child_list = skin_color_button_list, max_column = 3)

        self.mono_grid_layout = self.create_QGridLayout(w = self._width, nc = 5, parent = self.main_layout)
        self.mono_color_list = ['black', 'dark_grey', 'grey', 'light_grey', 'white']
        mono_color_button_list = []
        for color in self.mono_color_list:
            button = self.create_QPushButton(text = gen.compose_nice_name(color), bgc = self.color_rgb_dict[color],
                c = pall.Callback(self.assign_poly_shader_to_selection, color))
            mono_color_button_list.append(button)
        self.parent_QGridLayout(parent = self.mono_grid_layout, child_list = mono_color_button_list, max_column = 5)

        self.randomise_checkbox_grid_layout = self.create_QGridLayout(w = self._width, nc = 4, parent = self.main_layout)
        self.randomize_normal_checkBox = self.create_QCheckBox(text = 'Normal')
        self.randomize_light_checkBox = self.create_QCheckBox(text = 'Light', dv = True)
        self.randomize_skin_checkBox = self.create_QCheckBox(text = 'Skin')
        self.randomize_mono_checkBox = self.create_QCheckBox(text = 'Mono')
        randomize_checkbox_list = [self.randomize_normal_checkBox, self.randomize_light_checkBox, self.randomize_skin_checkBox, self.randomize_mono_checkBox]
        self.parent_QGridLayout(parent = self.randomise_checkbox_grid_layout, child_list = randomize_checkbox_list, max_column = 4)

        self.transparency_layout = self.create_QGridLayout(w = self._width, nc = 3, cwp = (20, 50, 30), parent = self.main_layout)
        self.parent_QGridLayout(parent = self.transparency_layout, child_list = [self.transparency_label, self.transparency_slider, self.transparency_spinBox], max_column = 3)

        self.randomize_button = self.create_QPushButton(text = 'Randomize Color', parent = self.main_layout, c = self.assign_randomize_poly_shader_to_selection)

        self.toggle_color_management = self.create_QPushButton(text = 'Toggle Color Management', parent = self.main_layout, c = gen.toggle_color_management)

    def transparency_slider_cc(self):
        val = self.transparency_slider.value()
        self.transparency_spinBox.setValue(val)

    def transparency_spinBox_cc(self):
        val = self.transparency_spinBox.value()
        self.transparency_slider.setValue(val)

def run():
    gui = Gui()
    gui.show()
