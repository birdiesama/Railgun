################################################################################
__Script__	= 'utils_RG.curve_blendshape_cv.core'
__Author__	= 'Weerapot Chaoman'
__Version__ = 2.2
__Date__	= 20200910
################################################################################
import os, sys, subprocess, webbrowser, re, inspect
import pymel.core as pm
import maya.OpenMayaUI as mui
from collections import OrderedDict
################################################################################
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
################################################################################

if not __self_path__ in sys.path:
    sys.path.insert(0, __self_path__)

from Qt import Qt, QtCore, QtGui, QtWidgets, QtCompat

import ui
reload (ui)
import general
reload (general)

def maya_main_window():
	main_window_ptr = mui.MQtUtil.mainWindow()
	return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class CvBlendshape(general.General):

	def __init__(self):
		super(CvBlendshape, self).__init__()

	def apply_cv_bs_btnCmd(self):
		# INFO from GUI

		pm.undoInfo(openChunk = True)

		lower_val = self.lower_val_spinBox.value()
		upper_val = self.upper_val_spinBox.value()
		bs_method = self.bs_method_comboBox.currentText()

		if upper_val > lower_val:
			direction = 1
		elif lower_val > upper_val:
			direction = -1
		else:
			direction = 0 # full blendshape

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

				driven_curve_shape_list = pm.listRelatives(driven_tfm, ad = True, type = 'nurbsCurve')
				driven_crv_list = list(set(pm.listRelatives(driven_curve_shape_list, parent = True)))

				if bs_method == 'Name Order':
					driver_crv_list = self.natural_sort(driver_crv_list)
					driven_crv_list = self.natural_sort(driven_crv_list)

				elif bs_method == 'Root Distance':
					curve_pair_list = self.get_closest_crv_pair_list(driver_crv_list, driven_crv_list)

				if not driven_tfm.hasAttr('_cv_bsn_'):
					pm.addAttr(driven_tfm, ln = '_cv_bsn_', at = 'double', k = True)
					driven_tfm._cv_bsn_.lock()

				if not driven_tfm.hasAttr('cv_bsn_src'):
					pm.addAttr(driven_tfm, ln = 'cv_bsn_src', dataType = 'string', keyable = True)
				driven_tfm.cv_bsn_src.unlock()
				driven_tfm.cv_bsn_src.set(driver_tfm.fullPath())
				driven_tfm.cv_bsn_src.lock()

				if not driven_tfm.hasAttr('cv_bsn_en'):
					pm.addAttr(driven_tfm, ln = 'cv_bsn_en', at = 'double', k = True, min = 0, max = 1, dv = 1)

				if bs_method == 'Name Order':

					for driver, driven in zip(driver_crv_list, driven_crv_list):
						blendshape = self.cv_blendshape(
							driver = driver, driven = driven, lower_val = lower_val, upper_val = upper_val, direction = direction)
						if not pm.isConnected(driven_tfm.cv_bsn_en, blendshape.en):
							driven_tfm.cv_bsn_en >> blendshape.en

				elif bs_method == 'Root Distance':

					for pair in curve_pair_list:
						driver, driven = pair
						blendshape = self.cv_blendshape(driver = driver, driven = driven, lower_val = lower_val, upper_val = upper_val, direction = direction)
						if not pm.isConnected(driven_tfm.cv_bsn_en, blendshape.en):
							driven_tfm.cv_bsn_en >> blendshape.en

		pm.undoInfo(closeChunk = True)

	def delete_cv_bs_btnCmd(self):

		pm.undoInfo(openChunk = True)

		selection_list = pm.ls(sl = True)

		bs_list = []
		src_list = []

		for selection in selection_list:
			if selection.hasAttr('cv_bsn_en'):
				bs_list = pm.listConnections(selection.cv_bsn_en)
				src_list.append(selection)
			else:
				nrb_crv_shp_list = pm.listRelatives(selection, ad = True, type = 'nurbsCurve')
				bs_list = pm.listConnections(nrb_crv_shp_list, type = 'blendShape')
				bs_list = list(set(bs_list))
				if bs_list:
					src_list = []
					for bs in bs_list:
						if '_cv_bsn' not in bs.nodeName():
							bs_list.remove(bs)
						else:
							src_list.extend(pm.listConnections(bs.envelope))
					src_list = list(set(src_list))

		if src_list:
			for src in src_list:
				for attr in ['_cv_bsn_', 'cv_bsn_src', 'cv_bsn_en']:
					if src.hasAttr(attr):
						exec('src.{0}.unlock()'.format(attr))
						exec('pm.deleteAttr(src.{0})'.format(attr))
			pm.delete(bs_list)

		pm.undoInfo(closeChunk = True)

class Gui(QtWidgets.QWidget, CvBlendshape, ui.UI):

	def __init__(self, parent = maya_main_window(), *args, **kwargs):

		super(Gui, self).__init__(parent)

		self._ui			= 'ui_hair_cv_blendshape'
		self._width 		= 350.00
		self._height		= 100.00
		self._title_name	= 'Hair CV BlendShape'
		self._title			= '{title_name} v{version}'.format(title_name = self._title_name, version = __Version__)

		self.delete_UI(self._ui)

		self.setObjectName(self._ui)
 		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True) # destroy this widget when close
		self.resize(self._width, self._height)
		self.setWindowTitle(self._title)
		self.setWindowFlags(QtCore.Qt.Window)
		self.setWindowModality(QtCore.Qt.NonModal)
		self.hair_diagram_image_path = __self_path__ + 'media/hair_CVBlendshape_hair.png'

 		self.gui_init()

	def gui_init(self):
		self.main_layout = self.create_QHBoxLayout(parent = self)

		self.framework_grid_layout = self.create_QGridLayout(parent = self.main_layout,
			h = self._height, nr = 1, w = self._width, cwp = (5, 35, 60))

		# Blendshape Bar
		self.blendshape_bar_label = self.create_QLabel(parent = self.framework_grid_layout, co = (0, 0))
		self.set_bs_bar_label(0.3, 0.7)

		# Hair diagram
		self.hair_diagram_vBox_layout = self.create_QVBoxLayout(parent = self.framework_grid_layout, co = (0, 1))
		self.hair_diagram_label = self.create_QLabel(parent = self.hair_diagram_vBox_layout)
		self.hair_diagram_pixmap = self.create_QPixmap(image_path = self.hair_diagram_image_path, parent = self.hair_diagram_label)
		self.hair_diagram_vBox_layout.setAlignment(QtCore.Qt.AlignCenter)
		self.hair_diagram_label.setScaledContents(True)

		# User Input
		self.user_input_vBox_layout = self.create_QVBoxLayout(parent = self.framework_grid_layout, co = (0, 2))
		self.user_input_vBox_layout.setAlignment(QtCore.Qt.AlignTop)
		self.user_input_grid_layout = self.create_QGridLayout(parent = self.user_input_vBox_layout, w = self._width / 10 * 6, nc = 2)

		self.lower_val_label = self.create_QLabel(text = 'Lower Val', parent = self.user_input_grid_layout, co = (0, 0))
		self.lower_val_spinBox = self.create_QSpinBox(range = (0, 100), step = 1, suffix = '%', value = 30,
			parent = self.user_input_grid_layout, co = (1, 0))

		self.upper_val_label = self.create_QLabel(text = 'Upper Val', parent = self.user_input_grid_layout, co = (0, 1))
		self.upper_val_spinBox = self.create_QSpinBox(range = (0, 100), step = 1, suffix = '%', value = 70,
			parent = self.user_input_grid_layout, co = (1, 1))

		self.lower_val_spinBox.valueChanged.connect(self.set_bs_bar_spinBox_cc)
		self.upper_val_spinBox.valueChanged.connect(self.set_bs_bar_spinBox_cc)

		# Buttons
		# self.bs_method_grid_layout = self.create_QGridLayout(w = self._width / 10 * 6, cwp = (40, 60),  parent = self.user_input_vBox_layout)
		self.bs_method_grid_layout = self.create_QGridLayout(w = self._width / 10 * 6, nc = 2,  parent = self.user_input_vBox_layout)

		self.bs_method_label = self.create_QLabel(text = 'Blendshape Method :', parent = self.bs_method_grid_layout, co = (0, 0))
		# bsn_option_list = ['Name Order']
		bsn_option_list = ['Name Order', 'Root Distance']
		self.bs_method_comboBox = self.create_QComboBox(item_list = bsn_option_list, parent = self.bs_method_grid_layout, co = (0, 1))

		self.create_bs_btn = self.create_QPushButton(text = 'Apply Blendshape', parent = self.user_input_vBox_layout, c = self.apply_cv_bs_btnCmd)
		self.delete_bs_btn = self.create_QPushButton(text = 'Delete Blendshape', parent = self.user_input_vBox_layout, c = self.delete_cv_bs_btnCmd)

	def set_bs_bar_label(self, lower_val, upper_val):
		lower_val = ((lower_val - 1.0) ** 2) ** 0.5
		upper_val = ((upper_val - 1.0) ** 2) ** 0.5
		color1 = 'GOLD'
		color2 = 'DIMGRAY'
		str_config = 'background-color: qlineargradient(x1:0 y1:{lower_val}, x2:0 y2:{upper_val},'.format(lower_val = lower_val, upper_val = upper_val)
		str_config += ' stop:0 {color2}, stop:1 {color1})'.format(color1 = color1, color2 = color2)
		self.blendshape_bar_label.setStyleSheet(str_config)

	def set_bs_bar_spinBox_cc(self):
		lower_val = self.lower_val_spinBox.value()
		upper_val = self.upper_val_spinBox.value()
		lower_val /= 100.00
		upper_val /= 100.00
		self.set_bs_bar_label(lower_val, upper_val)

def run():
	gui = Gui()
	gui.show()
