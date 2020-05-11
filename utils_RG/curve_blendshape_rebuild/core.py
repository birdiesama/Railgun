################################################################################
__Script__  = 'utils_RG.curve_blendshape_rebuild.core'
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

class CurveBlendshapeRebuild(general.General):

    def __init__(self):
        super(CurveBlendshapeRebuild, self).__init__()

    def curve_blendshape_rebuild(self):

        selection_list = pm.ls(sl = True)
        driver_tfm = selection_list[0]
        driven_tfm = selection_list[1]

        pair_list = self.get_closest_crv_pair_list(driver_tfm, driven_tfm)

        for pair in pair_list:
            driver = pair[0]
            driven = pair[1]

            driver_cv = self.get_curve_cv(driver)
            driven_cv = self.get_curve_cv(driven)

            driven_shape = self.get_visible_shape(driven)
            driven_degree = driven_shape.getAttr('degree')

            pm.rebuildCurve(driver,
                constructionHistory = True,
                replaceOriginal     = True,
                rebuildType         = 0, # uniform
                endKnots            = 1, # multiple end knots
                keepRange           = 0, # reparameterize the resulting curve from 0 to 1
                keepControlPoints   = False,
                keepEndPoints       = True,
                keepTangents        = True,
                spans               = driven_cv - driven_degree,
                degree              = driven_degree,
                tolerance           = 0.01,
                )

            self.quick_blendshape(driver, driven)

cbsr = CurveBlendshapeRebuild()

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class Gui(QtWidgets.QWidget, ui.UI):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(Gui, self).__init__(parent, *args, **kwargs)

        self._ui            = 'ui_curve_blendshape_rebuild'
        self._width         = 350.00
        self._height        = 10.00
        self._title_name    = 'Curve Bsh Rebuild'
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
        self.blendshape_label = self.create_QLabel(text = 'Select Driver, then Driven', parent = self.main_layout)
        self.blendshape_btn = self.create_QPushButton(text = 'Blendshape', parent = self.main_layout, c = self.blendshape_btnCmd)
        # nConstraint
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)

    def blendshape_btnCmd(self):
        pm.undoInfo(openChunk = True)
        cbsr.curve_blendshape_rebuild()
        pm.undoInfo(closeChunk = True)

def run():
    gui = Gui()
    gui.show()
