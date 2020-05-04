################################################################################
__Script__		= 'global_RG.general.module.misc'
__Author__		= 'Weerapot Chaoman'
__Version__		= 2.0
__Date__		= 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

class Misc(object):

    def __init__(self, *args, **kwargs):
        super(Misc, self).__init__(*args, **kwargs)

    def is_list(self, target_list):
        if not isinstance(target_list, list):
            target_list = [target_list]
        return target_list

    def get_distance(self, point1, point2):
        distance = ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2) ** 0.5
        return distance
