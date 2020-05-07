################################################################################
__Script__		= 'utils_RG.color_assignor_outliner.core'
__Author__		= 'Weerapot Chaoman'
__Version__		= 3.20
__Date__		= 20200506
################################################################################
import os, sys
import pymel.core as pm
import pymel.all as pall
import maya.OpenMayaUI as mui
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
def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class Gui(QtWidgets.QWidget, ui.UI):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(Gui, self).__init__(parent, *args, **kwargs)

        self.color_rgb_dict = gen.color_rgb_dict

        self._ui            = 'ui_color_assignor_outliner'
        self._width         = 350.00
        self._height        = 100.00
        self._title_name    = 'Outliner Color Assignor'
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
                c = pall.Callback(self.assign_outliner_color_to_selection, color))
            color_button_list.append(button)
        self.parent_QGridLayout(parent = self.color_grid_layout, child_list = color_button_list, max_column = 2)
        
        # appending disable button
        disable_layout = self.create_QVBoxLayout(parent = self.main_layout)
        self.create_QPushButton(text = 'Disable Outliner Color', c = self.disable_outliner_color_to_selection, parent = disable_layout)

    def assign_outliner_color_to_selection(self, color):
        selection_list = pm.ls(sl = True)
        gen.assign_outliner_color(target_list = selection_list, color_name = color)

    def disable_outliner_color_to_selection(self):
    	selection_list = pm.ls(sl = True)
    	for selection in selection_list:
    		selection.useOutlinerColor.set(0)


def run(*args, **kwargs):
    gui = Gui()
    gui.show()
