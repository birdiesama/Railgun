################################################################################
__Script__		= 'global_RG.general.module.outliner'
__Author__		= 'Weerapot Chaoman'
__Version__		= 2.0
__Date__		= 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import pymel.core as pm
################################################################################

class Outliner(object):

    def __init__(self, *args, **kwargs):
        super(Outliner, self).__init__(*args, **kwargs)

        self.outliner_color_dict = {}
        self.outliner_color_dict['green'] = (0.498039, 1, 0)
        self.outliner_color_dict['pale_green'] = (0.564706, 0.933333, 0.564706)
        self.outliner_color_dict['yellow'] = (1, 1, 0)
        self.outliner_color_dict['pale_yellow'] = (1, 0.870588, 0.678431)
        self.outliner_color_dict['red'] = (1, 0, 0)
        self.outliner_color_dict['pale_red'] = (0.803922, 0.360784, 0.360784)
        self.outliner_color_dict['pink'] = (1, 0.411765, 0.705882)
        self.outliner_color_dict['pale_pink'] = (0.941176, 0.501961, 0.501961)
        self.outliner_color_dict['purple'] = (1, 0, 1)
        self.outliner_color_dict['pale_purple'] = (0.866667, 0.627451, 0.866667)
        self.outliner_color_dict['light_blue'] = (0, 1, 1)
        self.outliner_color_dict['pale_blue'] = (0.529412, 0.807843, 0.980392)
        self.outliner_color_dict['white'] = (1, 1, 1)

    def outliner_color_disable(self, target_list):
        if not isinstance(target_list, list):
            target_list = [target_list]
        for target in target_list:
            target = pm.PyNode(target)
            target.useOutlinerColor.set(0)

    def outliner_color_apply(self, target_list, color='red'):
        if not isinstance(target_list, list):
            target_list = [target_list]
        for target in target_list:
            target = pm.PyNode(target)
            target.useOutlinerColor.set(1)
            target.outlinerColor.set(self.outliner_color_dict[color])
