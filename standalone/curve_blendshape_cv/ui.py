################################################################################
__Script__	= 'curve_blendshape_cv.ui'
__Author__  = 'Weerapot Chaoman'
__Date__    = 20200910
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
################################################################################
import subprocess, webbrowser, re, inspect
import pymel.core as pm
import maya.OpenMayaUI as mui
from collections import OrderedDict
from colorsys import rgb_to_hsv, hsv_to_rgb

if not __self_path__ in sys.path:
    sys.path.insert(0, __self_path__)

from Qt import Qt, QtCore, QtGui, QtWidgets, QtCompat
################################################################################

class Qt_UI(object):

    def __init__(self, *args, **kwargs):
        super(Qt_UI, self).__init__(*args, **kwargs)

    def get_rgb_complementary(self, rgb):
        r, g, b = rgb
        h, s, v = rgb_to_hsv(r, g, b)
        complementary = hsv_to_rgb((h + 0.5 % 1), s, v)
        return complementary

    def open_web(self, url):
           webbrowser.open(url, new=2) # new = 2 : open the url in the new tab in existing browser

    def delete_UI(self, ui):
        if pm.window(ui, ex=True):
            pm.deleteUI(ui)
            self.delete_UI(ui)

    def parent_QtWidgets(self, parent, child, co=None, label=None):
        attr_list = [
            'addLayout',
            'addTab',
            'addWidget',
            'setLayout',
            'setWidget',
            'setPixmap',
            ]

        if co:
            co = ', {co1}, {co2}'.format(co1 = co[0], co2 = co[1])
        else:
            co = ''

        if label: # for addTab
            label=", '{label}'".format(label = label)
        else:
            label = ''

        for attr in attr_list:
            if hasattr(parent, attr):
                try:
                    cmd = 'parent.{attr}(child{label}{co})'.format(attr = attr, co = co, label = label)
                    exec(cmd)
                except:
                    pass

    def parent_QGridLayout(self, parent, child_list, max_column=2):

        if not isinstance(child_list, list):
            child_list = [child_list]

        counter_x = 0
        counter_y = 0

        for child in child_list:
            if counter_x >= max_column:
                counter_x = 0
                counter_y += 1
            self.parent_QtWidgets(parent, child, co=(counter_y, counter_x))
            counter_x += 1

    def create_floatField(self, ui_name=None, label=None, min=None, max=None, dv=1.0, precision=None, parent=None, co=None):
        float_field = QtWidgets.QLineEdit()
        float_field.setAlignment(QtCore.Qt.AlignRight)
        validator = QtGui.QDoubleValidator()
        float_field.setValidator(validator)
        top_widget = float_field
        if label:
            layout = self.create_QHBoxLayout()
            label = self.create_QLabel(text = label, parent = layout)
            if ui_name:
                layout.setObjectName(ui_name + '_layout')
                label.setObjectName(ui_name + '_label')
            layout.addWidget(float_field)
            top_widget = layout
        if min:
            validator.setBottom(min)
        if max:
            validator.setTop(max)
        if dv:
            float_field.setText(str(dv))
        if precision:
            validator.setDecimals(precision)
        if ui_name:
            float_field.setObjectName(ui_name)
            validator.setObjectName(ui_name + '_validator')
        if parent:
            self.parent_QtWidgets(parent, top_widget, co = co)
        return(float_field)

    def create_intField(self, ui_name=None, label=None, min=None, max=None, dv=100, parent=None, co=None):
        int_field = QtWidgets.QLineEdit()
        int_field.setAlignment(QtCore.Qt.AlignRight)
        validator = QtGui.QIntValidator()
        int_field.setValidator(validator)
        top_widget = int_field
        if min:
            validator.setBottom(min)
        if max:
            validator.setTop(max)
        if dv:
            int_field.setText(str(dv))
        if ui_name:
            int_field.setObjectName(ui_name)
            validator.setObjectName(ui_name + '_validator')
        if parent:
            self.parent_QtWidgets(parent, top_widget, co = co)
        return(int_field)

    def create_separator(self, ui_name=None, parent=None, co=None):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        if ui_name:
            line.setObjectName(ui_name)
        if parent:
            self.parent_QtWidgets(parent, line, co = co)
        return(line)

    def create_filler(self, ui_name=None, parent=None, co=None):
        filler = QtWidgets.QLabel()
        if ui_name:
            filler.setObjectName(ui_name)
        if parent:
            self.parent_QtWidgets(parent, filler, co = co)
        return(filler)

    def create_QVBoxLayout(self, ui_name=None, parent=None, co=None):
        QVBoxLayout = QtWidgets.QVBoxLayout()
        if ui_name:
            QVBoxLayout.setObjectName(ui_name)
        if parent:
            self.parent_QtWidgets(parent, QVBoxLayout, co = co)
        return(QVBoxLayout)

    def create_QHBoxLayout(self, ui_name=None, parent=None, co=None):
        QHBoxLayout = QtWidgets.QHBoxLayout()
        if ui_name:
            QHBoxLayout.setObjectName(ui_name)
        if parent:
            self.parent_QtWidgets(parent, QHBoxLayout, co = co)
        return(QHBoxLayout)

    def create_QGridLayout(self, ui_name=None, parent=None, co=None, h=None, nr=None, rhp=None, w=None, nc=None, cwp=None):
        # rhp = Row Height Percentage
        # cwp = Column Width Percentage
        # nc and cwp requires w
        QGridLayout = QtWidgets.QGridLayout()
        if ui_name:
            QGridLayout.setObjectName(ui_name)
        if parent:
            self.parent_QtWidgets(parent, QGridLayout, co = co)

        # height
        if h:
            h = float(h)
        if nr:
            nr = int(nr)
            for i in range(0, nr):
                QGridLayout.setRowMinimumHeight(i, h / nr)
                QGridLayout.setRowStretch(i, 100 / nr)
        if rhp:
            nr = len(rhp)
            nr_sum = float(sum(rhp))
            for i in range (0, nr):
                QGridLayout.setRowMinimumHeight(i, h * (rhp[i] / nr_sum))
                QGridLayout.setRowStretch(i, rhp[i] / nr_sum * 100)

        # width
        if w:
            w = float(w) # just in case of division, for python 2
        if nc:
            nc = int(nc)
            for i in range(0, nc):
                QGridLayout.setColumnMinimumWidth(i, w / nc)
                QGridLayout.setColumnStretch(i, 100 / nc)
        if cwp:
            nc = len(cwp)
            nc_sum = float(sum(cwp))
            for i in range(0, nc):
                QGridLayout.setColumnMinimumWidth(i, w * (cwp[i] / nc_sum))
                QGridLayout.setColumnStretch(i, cwp[i] / nc_sum * 100)
        return(QGridLayout)

    def create_QLabel(self, ui_name=None, text=None, parent=None, co=None, alignment=None, word_wrap=None):
        QLabel = QtWidgets.QLabel()
        if ui_name:
            QLabel.setObjectName(ui_name)
        if text:
            QLabel.setText(text)
        if parent:
            self.parent_QtWidgets(parent, QLabel, co = co)
        if alignment:
            QLabel.setAlignment(alignment)
        if word_wrap:
            QLabel.setWordWrap(True)
        return(QLabel)

    def create_QPushButton(self, ui_name=None, text=None, expanding=None, parent=None, co=None, url=None, cmd=None, c=None, bgc=None):
        QPushButton = QtWidgets.QPushButton()
        if ui_name:
            QPushButton.setObjectName(ui_name)

        if text:
            text_QHBoxLayout = self.create_QHBoxLayout(parent = QPushButton)
            text_QLabel = self.create_QLabel(text = text, parent = text_QHBoxLayout)
            text_QLabel.setAlignment(QtCore.Qt.AlignCenter)
            text_QLabel.setWordWrap(True)
            text_QLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            text_QLabel.setMouseTracking(False)
            text_QLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            text_QHBoxLayout.setSpacing(0)
            text_QHBoxLayout.setMargin(0)

        if expanding:
            QPushButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        if parent:
            self.parent_QtWidgets(parent, QPushButton, co = co)

        if url:
            QPushButton.clicked.connect(lambda: self.open_web(url = url))

        if cmd:
            QPushButton.clicked.connect(cmd)
        if c:
            QPushButton.clicked.connect(c)
        if bgc:
            bgc = (bgc[0]*255, bgc[1]*255, bgc[2]*255)
            QPushButton.setStyleSheet('background-color:rgb({0},{1},{2})'.format(bgc[0], bgc[1], bgc[2]))
            if text:
                brightness = sum(bgc) / 3.0
                if brightness >= 127.5:
                    rgb = (0, 0, 0)
                else:
                    rgb = (255, 255, 255)
                text_QLabel.setStyleSheet('color:rgb({0},{1},{2})'.format(rgb[0], rgb[1], rgb[2]))
        return(QPushButton)

    def create_QScrollArea(self, ui_name=None, parent=None, vertical=True, horizontal=False, co=None):
        QScrollArea = QtWidgets.QScrollArea()
        if ui_name:
            QScrollArea.setObjectName(ui_name)
        if parent:
            self.parent_QtWidgets(parent, QScrollArea, co = co)
        if vertical:
            QScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        if horizontal:
            QScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        QScrollArea.setWidgetResizable(True)
        return QScrollArea

    def create_QTabWidget(self, ui_name=None, parent=None, co=None):
        QTabWidget = QtWidgets.QTabWidget()
        if ui_name:
            QTabWidget.setObjectName(ui_name)
        if parent:
            self.parent_QtWidgets(parent, QTabWidget, co = co)
        return QTabWidget

    def create_QWidget(self, ui_name=None, parent=None, co=None, label=None):
        QWidget = QtWidgets.QWidget()
        if ui_name:
            QWidget.setObjectName(ui_name)
        if parent:
            self.parent_QtWidgets(parent, QWidget, co = co, label = label)
        return QWidget

    def create_QPixmap(self, image_path, ui_name=None, parent=None, co=None):
        QPixmap = QtGui.QPixmap(image_path)
        if ui_name:
            QPixmap.setObjectName(ui_name)
        if parent:
            self.parent_QtWidgets(parent, QPixmap, co = co)
        return QPixmap

    def create_QSpinBox(self, ui_name=None, range=None, step=1, suffix=None, value=None, val=None, parent=None, co=None, cc=None):
        spin_box = QtWidgets.QSpinBox()
        spin_box.setSingleStep(step)
        if ui_name:
            spin_box.setObjectName(ui_name)
        if range:
            spin_box.setRange(range[0], range[1])
        if suffix:
            spin_box.setSuffix(suffix)
        if parent:
            self.parent_QtWidgets(parent, spin_box, co = co)
        if cc:
            spin_box.valueChanged.connect(cc)
        if value: spin_box.setValue(value)
        if val: spin_box.setValue(val)
        return spin_box

    def create_QDoubleSpinBox(self, ui_name=None, range=None, step=0.1, suffix=None, value=0.0, precision=2, parent=None, co=None):
        spin_box = QtWidgets.QDoubleSpinBox()
        spin_box.setSingleStep(step)
        spin_box.setValue(value)
        spin_box.setDecimals(precision)
        if ui_name:
            spin_box.setObjectName(ui_name)
        if range:
            spin_box.setRange(range[0], range[1])
        if suffix:
            spin_box.setSuffix(suffix)
        if parent:
            self.parent_QtWidgets(parent, spin_box, co = co)
        return spin_box

    def create_QComboBox(self, ui_name=None, item_list=None, parent=None, co=None):
        if not isinstance(item_list, list):
            item_list = [item_list]
        combo_box = QtWidgets.QComboBox()
        if ui_name:
            combo_box.setObjectName(ui_name)
        if item_list:
            for item in item_list:
                combo_box.addItem(str(item))
        if parent:
            self.parent_QtWidgets(parent, combo_box, co = co)
        return combo_box

    def create_QCheckBox(self, ui_name=None, text=None, dv=None, parent=None, co=None):
        check_box = QtWidgets.QCheckBox()
        if ui_name:
            check_box.setObjectName(ui_name)
        if text:
            check_box.setText(text)
        if dv:
            check_box.setCheckState(QtCore.Qt.CheckState.Checked)
        if parent:
            self.parent_QtWidgets(parent, check_box, co = co)
        return check_box

    def create_QHSlider(self, ui_name=None, min=None, max=None, val=None, value=None, dv=None, parent=None, co=None, cc=None, vc=None):
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        if ui_name:
            slider.setObjectName(ui_name)
        if min:
            slider.setMinimum(min)
        if max:
            slider.setMaximum(max)

        if val: slider.setValue(val)
        if value: slider.setValue(value)
        if dv: slider.setValue(dv)

        if parent:
            self.parent_QtWidgets(parent, slider, co = co)
        if cc: slider.valueChanged.connect(cc)
        if vc: slider.valueChanged.connect(vc)
        return slider

    def create_QLineEdit(self, ui_name=None, text=None, readOnly=False, read_only=None, ro=None, parent=None, co=None):
        lineEdit = QtWidgets.QLineEdit()
        if ui_name:
            lineEdit.setObjectName(ui_name)
        if text:
            lineEdit.setText(text)
        if readOnly or read_only or ro:
            lineEdit.setReadOnly(True)
        if parent:
            self.parent_QtWidgets(parent , lineEdit, co = co)
        return lineEdit

    def create_QListWidget(self, ui_name=None, min_w=None, max_w=None, min_h=None, max_h=None, ams=None, parent=None, co=None):
        # ams = allow multiple selection
        list_widget = QtWidgets.QListWidget()
        if ui_name:
            list_widget.setObjectName(ui_name)
        if min_w:
            list_widget.setMinimumWidth(min_w)
        if max_w:
            list_widget.setMaximumWidth(max_w)
        if min_h:
            list_widget.setMinimumHeight(min_h)
        if max_h:
            list_widget.setMaximumHeight(max_h)
        if ams:
            list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        if parent:
            self.parent_QtWidgets(parent, list_widget, co = co)
        
        return(list_widget)

    def get_QListWidget_items(self, widget):
        item_list = []
        for i in range(widget.count()):
            item_list.append(widget.item(i).text())
        return(item_list)

    def get_QListWidget_selectedItem(self, widget, raw=None):

        item_raw_list = widget.selectedItems()
        item_list = []
        for item in item_raw_list:
            if raw:
                item_list.append(item)
            else:
                item_list.append(item.text())
        return(item_list)

class UI(Qt_UI):
    
    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)