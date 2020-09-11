################################################################################
__Script__  = 'utils_RG.simulation_setup.core'
__Author__  = 'Weerapot Chaoman'
__Version__ = 2.00
__Date__    = 20200510
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


class FrameLayout(QtWidgets.QWidget):
    def __init__(self, parent=None, title=None):
        QtWidgets.QFrame.__init__(self, parent=parent)

        self._is_collasped = True
        self._title_frame = None
        self._content, self._content_layout = (None, None)

        self._main_v_layout = QtWidgets.QVBoxLayout(self)
        self._main_v_layout.addWidget(self.initTitleFrame(title, self._is_collasped))
        self._main_v_layout.addWidget(self.initContent(self._is_collasped))

        self.initCollapsable()

    def initTitleFrame(self, title, collapsed):
        self._title_frame = self.TitleFrame(title=title, collapsed=collapsed)

        return self._title_frame

    def initContent(self, collapsed):
        self._content = QtWidgets.QWidget()
        self._content_layout = QtWidgets.QVBoxLayout()

        self._content.setLayout(self._content_layout)
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsable(self):
        QtCore.QObject.connect(self._title_frame, QtCore.SIGNAL('clicked()'), self.toggleCollapsed)

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collasped)
        self._is_collasped = not self._is_collasped
        self._title_frame._arrow.setArrow(int(self._is_collasped))

    ############################
    #           TITLE          #
    ############################
    class TitleFrame(QtWidgets.QFrame):
        def __init__(self, parent=None, title="", collapsed=False):
            QtWidgets.QFrame.__init__(self, parent=parent)

            self.setMinimumHeight(24)
            self.move(QtCore.QPoint(24, 0))
            self.setStyleSheet("border:1px solid rgb(41, 41, 41); ")

            self._hlayout = QtWidgets.QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._hlayout.setSpacing(0)

            self._arrow = None
            self._title = None

            self._hlayout.addWidget(self.initArrow(collapsed))
            self._hlayout.addWidget(self.initTitle(title))

        def initArrow(self, collapsed):
            self._arrow = FrameLayout.Arrow(collapsed=collapsed)
            self._arrow.setStyleSheet("border:0px")

            return self._arrow

        def initTitle(self, title=None):
            self._title = QtWidgets.QLabel(title)
            self._title.setMinimumHeight(24)
            self._title.move(QtCore.QPoint(24, 0))
            self._title.setStyleSheet("border:0px")

            return self._title

        def mousePressEvent(self, event):
            self.emit(QtCore.SIGNAL('clicked()'))

            return super(FrameLayout.TitleFrame, self).mousePressEvent(event)


    #############################
    #           ARROW           #
    #############################
    class Arrow(QtWidgets.QFrame):
        def __init__(self, parent=None, collapsed=False):
            QtWidgets.QFrame.__init__(self, parent=parent)

            self.setMaximumSize(24, 24)

            # horizontal == 0
            self._arrow_horizontal = (QtCore.QPointF(7.0, 8.0), QtCore.QPointF(17.0, 8.0), QtCore.QPointF(12.0, 13.0))
            # vertical == 1
            self._arrow_vertical = (QtCore.QPointF(8.0, 7.0), QtCore.QPointF(13.0, 12.0), QtCore.QPointF(8.0, 17.0))
            # arrow
            self._arrow = None
            self.setArrow(int(collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir:
                self._arrow = self._arrow_vertical
            else:
                self._arrow = self._arrow_horizontal

        def paintEvent(self, event):
            painter = QtWidgets.QPainter()
            painter.begin(self)
            painter.setBrush(QtWidgets.QColor(192, 192, 192))
            painter.setPen(QtWidgets.QColor(64, 64, 64))
            painter.drawPolygon(*self._arrow)
            painter.end()

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class Gui(QtWidgets.QWidget, ui.UI):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(Gui, self).__init__(parent, *args, **kwargs)

        self._ui            = 'ui_simulation_set_up_util'
        self._width         = 400.00
        self._height        = 10.00
        self._title_name    = 'Simulation Setup Util'
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

        f = FrameLayout(title = 'fuck my life')
        self.create_QPushButton(parent = f)
        self.main_layout.addWidget(f)

def run():
    gui = Gui()
    gui.show()

# app = QtWidgets.QApplication(sys.argv)

# win = QtWidgets.QMainWindow()
# w = QtWidgets.QWidget()
# w.setMinimumWidth(350)
# win.setCentralWidget(w)
# l = QtWidgets.QVBoxLayout()
# l.setSpacing(0)
# l.setAlignment(QtCore.Qt.AlignTop)
# w.setLayout(l)

# t = FrameLayout(title="Buttons")
# t.addWidget(QtWidgets.QPushButton('a'))
# t.addWidget(QtWidgets.QPushButton('b'))
# t.addWidget(QtWidgets.QPushButton('c'))

# f = FrameLayout(title="TableWidget")
# rows, cols = (6, 3)
# data = {'col1': ['1', '2', '3', '4', '5', '6'],
#         'col2': ['7', '8', '9', '10', '11', '12'],
#         'col3': ['13', '14', '15', '16', '17', '18']}
# table = QtWidgets.QTableWidget(rows, cols)
# headers = []
# for n, key in enumerate(sorted(data.keys())):
#     headers.append(key)
#     for m, item in enumerate(data[key]):
#         newitem = QtWidgets.QTableWidgetItem(item)
#         table.setItem(m, n, newitem)
# table.setHorizontalHeaderLabels(headers)
# f.addWidget(table)

# l.addWidget(t)
# l.addWidget(f)

# win.show()
# win.raise_()
# print "Finish"
# sys.exit(app.exec_())

