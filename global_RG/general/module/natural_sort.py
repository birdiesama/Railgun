################################################################################
__Script__		= 'global_RG.general.module.natural_sort'
__Author__		= 'Weerapot Chaoman'
__Version__		= 2.0
__Date__		= 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import re
################################################################################

class NaturalSort(object):
    def __init__(self, *args, **kwargs):
        super(NaturalSort, self).__init__(*args, **kwargs)

    def convert_key_elem(self, input):
        if input.isdigit(): return int(input)
        else: return input.lower()

    def split_key(self, key):
        return_list = []
        key = str(key)
        for elem in re.split('([0-9]+)', key):
            return_list.append(self.convert_key_elem(elem))
        return return_list

    def natural_sort(self, list):
        return sorted(list, key = self.split_key)
