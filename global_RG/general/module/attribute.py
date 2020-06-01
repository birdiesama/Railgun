################################################################################
__Script__		= 'global_RG.general.module.alembic'
__Author__		= 'Weerapot Chaoman'
__Version__		= 2.00
__Date__		= 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

import pymel.core as pm
import re

class Attribute(object):

    def __init__(self, *args, **kwargs):
        # super(Attribute, self).__init__(*args, **kwargs)
        super(Attribute, self).__init__()

    def get_selected_attributes(self):
        selection_list = pm.ls(sl = True)
        selection = selection_list[0]
        current_channel_box = pm.mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
        main_attr       = pm.channelBox(current_channel_box, q = True, sma = True)
        history_attr    = pm.channelBox(current_channel_box, q = True, sha = True)
        output_attr     = pm.channelBox(current_channel_box, q = True, soa = True)
        shape_attr      = pm.channelBox(current_channel_box, q = True, ssa = True)
        selected_attr = []
        if main_attr:
            selected_attr.extend(main_attr)
        if history_attr:
            selected_attr.extend(history_attr)
        if output_attr:
            selected_attr.extend(output_attr)
        if shape_attr:
            selected_attr.extend(shape_attr)
        return_list = []
        for attr in selected_attr:
            attr = pm.PyNode(selection + '.' + attr)
            return_list.append(attr)
        return return_list

    def get_attribute_increment(self, node, input_str):
        node = pm.PyNode(node)
        all_attr_list = node.listAttr(userDefined = True)
        attr_list = []
        regex = re.compile(r'{0}[0-9]+'.format(input_str))
        for attr in all_attr_list:
            if regex.findall(attr.attrName()):
                attr_list.append(attr)
        attr_list = self.natural_sort(attr_list)

        if attr_list:
            latest_increment = attr_list[-1]
            latest_increment = re.findall(r'[0-9]+', str(latest_increment))[-1]
            new_increment = int(latest_increment) + 1
            return(new_increment)
        else:
            print('no matching attribute exists, returning 1')
            return(1)

    ##################
    ''' lock hide attr '''
    ##################
    def lock_hide_attr(self, target, attr_list=None, en=True):
        
        channelBox_val = not en
        keyable_val = not en
        lock_val = en

        # patch
        target_list = target
        if not isinstance(target_list, list):
            target_list = [target_list]
        target = None
        
        for target in target_list:

            target = pm.PyNode(target)

            if not attr_list:
                for attr in ['t', 'r', 's']:
                    for axis in ['x', 'y', 'z']:
                        if en:
                            pm.setAttr(target + '.' + attr + axis, keyable = keyable_val)
                            pm.setAttr(target + '.' + attr + axis, channelBox = channelBox_val)
                            self.lock_default_attr(target, en = en)
                        elif not en:
                            pm.setAttr(target + '.' + attr + axis, channelBox = channelBox_val)
                            pm.setAttr(target + '.' + attr + axis, keyable = keyable_val)
                            self.lock_default_attr(target, en = en)

            else:
                for attr in attr_list:
                    if attr in ['t', 'r', 's']:
                        for axis in ['x', 'y', 'z']:
                            if en:
                                pm.setAttr(target + '.' + attr + axis, keyable = keyable_val)
                                pm.setAttr(target + '.' + attr + axis, channelBox = channelBox_val)
                            elif not en:
                                pm.setAttr(target + '.' + attr + axis, channelBox = channelBox_val)
                                pm.setAttr(target + '.' + attr + axis, keyable = keyable_val)
                    else:
                        if en:
                            pm.setAttr(target + '.' + attr, keyable = keyable_val)
                            pm.setAttr(target + '.' + attr, channelBox = channelBox_val)
                        elif not en:
                            pm.setAttr(target + '.' + attr, channelBox = channelBox_val)
                            pm.setAttr(target + '.' + attr, keyable = keyable_val)

                self.lock_attr(target, attr_list = attr_list, en = en)

    def lock_default_attr(self, target, en=True):
        if en: lock = 'lock'
        else: lock = 'unlock'
        target = pm.PyNode(target)
        for attr in ['t', 'r', 's']:
            exec('target.{attr}.{lock}()'.format(attr = attr, lock = lock))
            for axis in ['x', 'y', 'z']:
                exec('target.{attr}{axis}.{lock}()'.format(attr = attr, axis = axis, lock = lock))

    def lock_attr(self, target, attr_list=None, en=True):
        if en: lock = 'lock'
        else: lock = 'unlock'
        target = pm.PyNode(target)
        if attr_list:
            for attr in attr_list:
                exec('target.{attr}.{lock}()'.format(attr = attr, lock = lock))
                if attr in ['t', 'r', 's']:
                    for axis in ['x', 'y', 'z']:
                        exec('target.{attr}{axis}.{lock}()'.format(attr = attr, axis = axis, lock = lock))
