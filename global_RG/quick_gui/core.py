################################################################################
__Script__          = 'global_RG.quick_gui.core'
__Author__          = 'Weerapot Chaoman'
__Version__         = 3.00
__Date__            = 20200504
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
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
import subprocess, webbrowser, re, inspect
import pymel.core as pm
import maya.OpenMayaUI as mui
from collections import OrderedDict
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

class _Url(object):
    # requires _ComposeName class

    def __init__(self, *args, **kwargs):
        super(_Url, self).__init__()

        url_path = __self_path__ + '__dir'
        file_list = os.listdir(url_path)
        file_list.sort()

        self._url_list = []

        for file in file_list:

            name_split = file.split('__')[-1]
            name_split = name_split.split('.txt')[0]
            name = self.compose_nice_name(name_split)

            text_file = open('{0}/{1}'.format(url_path, file), 'r')
            url = text_file.read()
            text_file.close()

            self._url_list.append([name, url])

class _OpenDir(object):
    # requires _ComposeName class

    def __init__(self, *args, **kwargs):
        super(_OpenDir, self).__init__()

        dir_path = __self_path__ + '__url'
        file_list = os.listdir(dir_path)
        file_list.sort()

        self._path_list = []

        for file in file_list:

            name_split = file.split('__')[-1]
            name_split = name_split.split('.txt')[0]
            name = self.compose_nice_name(name_split)

            text_file = open('{0}/{1}'.format(dir_path, file), 'r')
            path = text_file.read()
            text_file.close()

            self._path_list.append([name, path])

    def _open_path(self, path):
        subprocess.Popen(['xdg-open', path])

    def open_path_QPushButton(self, name, path):
        snake_case_name = self.compose_snake_case(name)
        nice_name = self.compose_nice_name(name)
        QPushButton = QtWidgets.QPushButton()
        QPushButton.setObjectName(snake_case_name + '_QPushButton_ui')
        QPushButton.setText(nice_name)
        QPushButton.clicked.connect(lambda: self._open_path(path=path))
        return QPushButton

class _SpecialCase(object):

    def __init__(self, *args, **kwargs):
        super(_SpecialCase, self).__init__()

        self.special_case_dict = {}

        # self.special_case_dict['name.py'] = self.name_btnCmd
        # def name_btnCmd(self): content...

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class QuickGui(_SpecialCase, _Url, _OpenDir, QtWidgets.QWidget, general.General, ui.UI):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(QuickGui, self).__init__(parent)

        self._ui            = 'quick_gui_ui'
        self._width         = 1000.00
        self._height        = 800.00
        self._version       = __Version__
        self._title_name    = 'Quick Gui'
        self._title         = '{titleName} v{version}'.format(titleName=self._title_name, version=self._version)

        self.delete_UI(self._ui)

        self.setObjectName(self._ui)
        self.resize(self._width, self._height)
        self.setWindowTitle(self._title)
        self.setWindowFlags(QtCore.Qt.Window)

        self.main_QVBoxLayout = self.create_QVBoxLayout(parent = self)

        ##################
        ''' LOCATION '''
        ##################

        self._project = 'Railgun'
        self._project_suffix = '_RG'  # This should be unique in your path string

        text_path = '{0}__public_path.txt'.format(__self_path__)
        text_file = open(text_path, 'r')
        text = text_file
        text_file.close()
        self._public_path = r'{0}'.format(text)
        self._status = None

        self._self_path = os.path.realpath(__file__)
        self._file_name = os.path.basename(__file__)
        self._self_path = self._self_path.replace(self._file_name, '')
        self._self_path = self._self_path.replace('\\', '/')

        self._my_path = None
        self._private_path = None

        if self._public_path in self._self_path:
            self._status = 'PUBLIC'
            self._my_path = self._public_path
            self._splitter = ''
        else:
            self._status = 'PRIVATE'
            self._my_path = self._self_path.split(self._project)[0]
            self._private_path = self._my_path
            self._my_path += self._project
            self._my_path += '/'
            self._splitter = self._project

        self._ignore_list = ['__init__.py', 'quickGui', 'html']

        self._module_list = ['global_RG', 'nucleus_RG', 'project_RG', 'qualoth_RG', 'test_RG', 'utils_RG', 'ziva_RG', 'external_RG']
        self._general_module_list = ['utils_RG', 'nucleus_RG', 'external_RG', 'resource_RG', 'legacy_RG', 'wip_RG']

        ##################
        ''' WIKI '''
        ##################
        # self.wiki_QGridLayout = self.create_QGridLayout(parent = self.main_QVBoxLayout)
        # self.help_QPushButton = self.create_QPushButton(text = 'Wiki', parent = self.main_QVBoxLayout, url = '') # wiki button

        ##################
        ''' TAB '''
        ##################
        self.tab_QGridLayout = self.create_QGridLayout(parent = self.main_QVBoxLayout)
        self.tab_LFT_QWidget = self.create_QWidget(parent = self.tab_QGridLayout, co = (0, 0))
        self.tab_RGT_QWidget = self.create_QWidget(parent = self.tab_QGridLayout, co = (0, 1))

        ##################
        ''' LEFT TAB '''
        ##################
        self.project_QVBoxLayout = self.create_QVBoxLayout(parent = self.tab_LFT_QWidget)
        self.project_QLabel = self.create_QLabel(text = 'Project Utilities', parent = self.project_QVBoxLayout)
        self.project_QTabWidget = self.create_QTabWidget(parent = self.project_QVBoxLayout)
        project_list = os.listdir(self._my_path + 'project_RG')
        for project in project_list:
            if project not in self._ignore_list and '.pyc' not in project:
                self._create_tool_tabs(
                    dir        = project,
                    path    = self._my_path + 'project_RG' + '/',
                    parent    = self.project_QTabWidget,
                    )
        self.project_QVBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        ####################
        ''' RIGHT TAB '''
        ####################
        self.general_QVBoxLayout = self.create_QVBoxLayout(parent = self.tab_RGT_QWidget)
        self.general_QLabel = self.create_QLabel(text = 'General Utilities', parent = self.general_QVBoxLayout)
        self.general_QTabWidget = self.create_QTabWidget(parent = self.general_QVBoxLayout)
        for generalUtil in self._general_module_list:
            self._create_tool_tabs(
                dir=generalUtil,
                path=self._my_path,
                parent=self.general_QTabWidget,
                )
        self.general_QVBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        ########################################
        ''' Quality of Life '''
        ########################################

        self.qof_QGridLayout = self.create_QGridLayout(parent = self.main_QVBoxLayout)

        QPushButton_list =[]
        for item_list in [self._url_list, self._path_list]:
            for item in item_list:
                QPushButton_list.append(self.create_QPushButton(text = item[0], url = item[1]))

        self.parent_QGridLayout(self.qof_QGridLayout, QPushButton_list, max_column = 3)
        self.qof_QGridLayout.setAlignment(QtCore.Qt.AlignTop)

    def _create_tool_tabs(self, dir, path, parent):

        QtWidget_top = self.create_QWidget(parent = parent, label = dir)
        QVBoxLayout_top = self.create_QVBoxLayout(parent = QtWidget_top)
        QScrollArea = self.create_QScrollArea(parent = QVBoxLayout_top)
        QtWidget = self.create_QWidget(parent = QScrollArea)
        QVBoxLayout = self.create_QVBoxLayout(parent = QtWidget)

        tool_list = os.listdir(path + dir)
        for tool in tool_list:
            if '.pyc' in tool:
                tool_list.remove(tool)
        tool_list = self.natural_sort(tool_list)

        for tool in tool_list:

            if (tool not in self._ignore_list):  # screen out unwanted, wip module
                tool_name = tool.split('.py')[0]

                tool_nice_name = self.compose_nice_name(tool_name)

                if tool in self.special_case_dict.keys():  # The one that is not normally compatible with the quick gui
                    QPushButton = self.create_QPushButton(text = tool_nice_name, parent = QVBoxLayout, cmd = self.special_case_dict[tool])

                else:  # See if this script is run from a private or public workspace
                    if self._status == 'PRIVATE':
                        if self._private_path not in sys.path:
                            sys.path.insert(0, self._private_path)
                    elif self._status == 'PUBLIC':
                        pass
                    else:
                        pm.error('>>> Please check where you run this script from ... script terminated')

                    path_to_tool = path + dir

                    # Create import command

                    cmd = 'import '
                    if self._status == 'PRIVATE':
                        cmd += self._project + '.'

                    path_split = path_to_tool.split(self._splitter)[-1]
                    if path_split != '/':
                        path_split_list = path_split.split('/')
                    path_split_list = self.list_remove_blank(path_split_list)

                    cmd += path_split_list[0]

                    for path_split in path_split_list[1:]:
                        cmd += '.'
                        cmd += path_split

                    # Will determine how to create the cmd and button
                    try:
                        # if tool_name == 'general':
                        exec('{cmd}.{tool_name} as gq_{tool_name}'.format(cmd = cmd, tool_name = tool_name))
                        exec('tool_proxy = gq_{tool_name}'.format(tool_name = tool_name))

                        if not hasattr(tool_proxy, 'run'):
                            try:
                                exec('{cmd}.{tool_name}.core as gq_{tool_name}'.format(cmd = cmd, tool_name = tool_name))
                                exec('tool_proxy = gq_{tool_name}'.format(tool_name = tool_name))
                            except:
                                pass

                        exec('reload(gq_{tool_name})'.format(tool_name = tool_name))

                        if hasattr(tool_proxy, 'run'):  # When the module has 'run', create this normally
                            cmd = 'btnCmd = gq_{tool_name}.run'.format(tool_name=tool_name)
                            exec(cmd)
                            QPushButton = self.create_QPushButton(text = tool_nice_name, cmd = btnCmd, parent = QVBoxLayout)
                            print('>>>>>> [ {tool_name} ] auto connect successful'.format(tool_name=tool_name))

                        elif hasattr(tool_proxy, 'QuickGuiChild'):  # When you have quick gui child
                            quick_qui_child = tool_proxy.QuickGuiChild()
                            child_cmd_list = []
                            for member in inspect.getmembers(tool_proxy):
                                if inspect.isfunction(member[1]):
                                    if member[0][-7:] == '_btnCmd':
                                        child_cmd_list.append(member[0])

                            child_QWidget = self.create_QWidget(parent = QVBoxLayout)
                            child_QVBoxLayout = self.create_QVBoxLayout(parent = child_QWidget)

                            child_QLabel = self.create_QLabel(text = tool_nice_name, parent = child_QVBoxLayout)
                            child_QLabel.setAlignment(QtCore.Qt.AlignCenter)

                            child_QGridLayout = self.create_QGridLayout(parent = child_QVBoxLayout)

                            child_cmd_list = self.natural_sort(child_cmd_list)

                            QPushButton_list = []

                            for child_cmd in child_cmd_list:
                                btn_name = child_cmd
                                orderControl = re.compile('__[0-9]+__') # sneaked in "order control"
                                orderControl_mo = orderControl.findall(btn_name)
                                if orderControl_mo:
                                    btn_name = btn_name.replace(orderControl_mo[0], '')
                                btn_name = self.compose_nice_name(btn_name.replace('_btnCmd', ''))
                                exec('btn_cmd = gq_{tool_name}.{child_cmd}'.format(tool_name = tool_name, child_cmd = child_cmd))
                                QPushButton = self.create_QPushButton(text = btn_name, cmd = btn_cmd)
                                QPushButton_list.append(QPushButton)

                            self.parent_QGridLayout(child_QGridLayout, QPushButton_list, max_column = quick_qui_child.column)
                            child_QGridLayout.setAlignment(QtCore.Qt.AlignTop)

                    except:  # When everything fail
                        QPushButton = self.create_QPushButton(text = tool_nice_name, parent = QVBoxLayout)
                        QPushButton.setStyleSheet('background-color : black')
                        print('>>!!>> [ {tool_name} ] cannot be connected'.format(tool_name=tool_name))

        QVBoxLayout.setAlignment(QtCore.Qt.AlignTop)

def run(*args, **kwargs):
    gui = QuickGui()
    gui.show()
