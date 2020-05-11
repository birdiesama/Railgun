################################################################################
__Script__  = 'utils_RG.curve_builder.core'
__Author__	= 'Weerapot Chaoman'
__Version__	= 1.10
__Date__	= 20200510
################################################################################
import os, re, sys
import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMayaUI as mui
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

class CurveBuilder(general.General):

    def __init__(self):
        super(CurveBuilder, self).__init__()

    def create_straight_curve(self, posA, posB, cv=10):
        pos_list = []

        step = []
        for i in range(0, 3):
            step.append((posB[i] - posA[i]) / float(cv-1))

        for i in range(0, cv):
            pos = []
            for axis in range(0, 3):
                pos.append(posA[axis] + (step[axis] * i))
            pos_list.append(pos)

        for pos in pos_list:
            print pos

        pm.curve(d = 1, p = pos_list)

cb = CurveBuilder()

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class Gui(QtWidgets.QWidget, ui.UI):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(Gui, self).__init__(parent, *args, **kwargs)

        self._ui            = 'ui_curve_builder'
        self._width         = 300.00
        self._height        = 10.00
        self._title_name    = 'Curve Builder'
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

        # create straight curve
        self.create_QLabel(text = 'Select 2 transforms, input number of CV, press the button', parent = self.main_layout)
        grid = self.create_QGridLayout(parent = self.main_layout, w = self._width, nc = 3, cwp = (25, 25, 50))
        self.create_straight_curve_label = self.create_QLabel(text = 'Number of CV')
        self.create_straight_curve_intField = self.create_intField(dv = 10)
        self.create_straight_curve_btn = self.create_QPushButton(text = 'Create Straight Curve', c = self.create_straight_curve_btnCmd)
        self.parent_QGridLayout(parent = grid, child_list = [self.create_straight_curve_label, self.create_straight_curve_intField, self.create_straight_curve_btn], max_column = 3)

        self.main_layout.setAlignment(QtCore.Qt.AlignTop)

    def create_straight_curve_btnCmd(self):

        selection_list = pm.ls(sl = True)
        if len(selection_list) != 2:
            pm.warning('... Create straight curve function requires user to select 2 transforms')
        else:
            posA = selection_list[0]
            posA = pm.xform(posA, q = True, rp = True, ws = True)
            posB = selection_list[1]
            posB = pm.xform(posB, q = True, rp = True, ws = True)
            cv = int(self.create_straight_curve_intField.text())
            cb.create_straight_curve(posA, posB, cv)


def run(*args, **kwargs):
    gui = Gui()
    gui.show()
