################################################################################
__Script__          = 'global_RG.general.module.clean_up'
__Author__          = 'Weerapot Chaoman'
__Version__         = 2.0
__Date__            = 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import pymel.core as pm
################################################################################

class Create(object):

    def __init__(self):
        super(Create, self).__init__()

    def create_group(self, name=None, parent=None, rgb=None, color=None, lock=None, lock_hide=None):
        if name: # name
            if not pm.objExists(name):
                grp = pm.group(em = True, w = True, name = name)
            else:
                grp = pm.PyNode(name)
        else:
            grp = pm.group(em = True, w = True)
        if parent: # parent
            if grp.getParent() != parent:
                pm.parent(grp, parent)
        if rgb: # color
            if not isinstance(rgb, tuple):
                rgb = self.color_rgb_dict[rgb] # general.color
            grp.useOutlinerColor.set(True)
            grp.outlinerColor.set(rgb[0], rgb[1], rgb[2])
        if color:
            if not isinstance(color, tuple):
                rgb = self.color_rgb_dict[color] # general.color
            else:
                rgb = color
            grp.useOutlinerColor.set(True)
            grp.outlinerColor.set(rgb[0], rgb[1], rgb[2])
        if lock: # lock
            self.lock_default_attr(grp) #general.clean_up
        if lock_hide: # lock_hide
            self.lock_hide_attr(grp) #general.clean_up
        return(grp)

    def create_set(self, name=None):
        if name: # name
            if not pm.objExists(name):
                set_node = pm.sets(em = True, n = name)
            else:
                set_node = pm.PyNode(name)
        else:
            set_node = pm.sets(em = True)
        return(set_node)

    def create_display_layer(self, name=None, rgb=None):
        if name: # name
            if not pm.objExists(name):
                display_layer = pm.createDisplayLayer(n = name)
            else:
                display_layer = pm.PyNode(name)
        else:
            display_layer = pm.createDisplayLayer()

        display_layer.displayType.set(0)

        if rgb: # color
            if not isinstance(rgb, tuple):
                rgb = self.color_rgb_dict[rgb] # general.color
            display_layer.overrideColorRGB.set(rgb)
            display_layer.overrideRGBColors.set(True)
        return(display_layer)
