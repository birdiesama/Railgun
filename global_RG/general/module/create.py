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

    def create_namespace(self, name=None):
        # doesn't create anything if no name
        if name:
            if not pm.namespace(exists = name):
                pm.namespace(add = name)
        return(name)

    def create_locator(self, name=None):
        if name:
            if not pm.objExists(name):
                locator = pm.spaceLocator(n = name, p = [0, 0, 0])
            else:
                locator = pm.PyNode(name)
        else:
            locator = pm.spaceLocat(p = [0, 0, 0])
        return(locator)

    def create_mdv(self, name=None, mode=None):
        mode_dict = {}
        mode_dict['no operation'] = 0
        mode_dict['multiply'] = 1
        mode_dict['divide'] = 2
        mode_dict['power'] = 3

        if name:
            if not pm.objExists(name):
                mdv = pm.createNode('multiplyDivide', n = name)
            else:
                mdv = pm.PyNode(name)
        else:
            mdv = pm.createNode('multiplyDivide')
        
        if mode:
            if type(mode) == type('str'):
                mode = mode_dict[mode]
            mdv.op.set(mode)

        return(mdv)

    def create_pma(self, name=None, mode=None):
        mode_dict = {}
        mode_dict['no operation'] = 0
        mode_dict['sum'] = 1
        mode_dict['add'] = 1
        mode_dict['subtract'] = 2
        mode_dict['minus'] = 2
        mode_dict['average'] = 3

        if name:
            if not pm.objExists(name):
                pma = pm.createNode('plusMinusAverage', n = name)
            else:
                pma = pm.PyNode(name)
        else:
            pma = pm.createNode('plusMinusAverage')

        if mode:
            if type(mode) == type('str'):
                mode = mode_dict[mode]
            pma.op.set(mode)
        
        return(pma)

    def create_clamp(self, name=None, max=None, min=None):

        if name:
            if not pm.objExists(name):
                clamp = pm.createNode('clamp', n = name)
            else:
                clamp = pm.PyNode(name)
        if max:
            clamp.max.set(max, max, max)
        if min:
            clamp.min.set(min, min, min)

        return(clamp)
  





