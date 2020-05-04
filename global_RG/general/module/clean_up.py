################################################################################
__Script__  = 'global_RG.general.module.clean_up'
__Author__  = 'Weerapot Chaoman'
__Version__ = 2.0
__Date__    = 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import pymel.core as pm
################################################################################

class CleanUp(object):
    def __init__(self):
        super(CleanUp, self).__init__()

    def delete_non_visible_shape(self, target):
        target = pm.PyNode(target)
        target_shape_list = target.getShapes()
        for target_shape in target_shape_list:
            if target_shape.isIntermediate():
                pm.delete(target_shape)
        target_shape = target.getShape()
        target_shape.rename(target.nodeName() + 'Shape')

    def freeze_transform(self, target):
        target = pm.PyNode(target)
        pm.makeIdentity(target, apply = True)

    def delete_history(self, target):
        target = pm.PyNode(target)
        pm.delete(target, ch = True)

    def center_pivot(self, target):
        target = pm.PyNode(target)
        pm.xform(target, cp = True)

    def list_connections(self, target, type):
        # list connections of the transform + it's shapes for specified connection type
        connection_list = []
        target = pm.PyNode(target)
        target_shape_list = target.getShapes()
        connection_list.extend(target.listConnections(type = type))
        for target_shape in target_shape_list:
            connection_list.extend(target_shape.listConnections(type = type))
        return connection_list

    def get_visible_shape(self, mesh):
        mesh = pm.PyNode(mesh)
        try:
            mesh_shape = mesh.getShape()
            if mesh_shape.isIntermediate():  # It's not the shape we see? Lets run through every shape and see
                mesh_shape_list = mesh.getShapes()
                for mesh_shape_prx in mesh_shape_list:
                    if not mesh_shape_prx.isIntermediate():
                        mesh_shape = mesh_shape_prx
            return mesh_shape
        except:
            return None

    ##################
    ''' lock hide attr '''
    ##################
    def lock_hide_attr(self, target, attr_list=None, en=True):
        channelBox_val = not en
        keyable_val = not en
        lock_val = en
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

    ##################
    ''' sets '''
    ##################
    def remove_from_set(self, object_set_list, object_list):
        target_list = []
        for object in object_list:
            target_list.append(object)
            try:
                target_list.extend(object.getShapes())
            except:
                pass
        for object_set in object_set_list:
            pm.sets(object_set, rm = target_list)

    def remove_from_all_set(self, target):
        target = pm.PyNode(target)
        target_shape_list = target.getShapes()

        target_list = [target]
        target_list.extend(target_shape_list)

        set_list = []
        set_list.extend(target.listConnections(type = 'objectSet'))

        for target_shape in target_shape_list:
            set_list.extend(target_shape.listConnections(type = 'objectSet'))
        set_list = list(set(set_list))

        for set_name in set_list:
            pm.sets(set_name, rm = target_list)

    def add_to_set(self, list_object, list_object_set):

        list_target = []

        for object in list_object:
            list_target.append(object)
            # if self.get_visible_shape(object):
            #     list_target.append(self.get_visible_shape(object))

        for set_name in list_object_set:
            pm.sets(set_name, add=list_target)

    ##################
    ''' layer '''
    ##################
    def remove_from_all_layer(self, target):
        target = pm.PyNode(target)
        target_list = []
        target_list.append(target)
        target_list.append(target.getShapes())
        for item in target_list:
            pm.editDisplayLayerMembers('defaultLayer', item)

    ##################
    ''' unlock normal '''
    ##################
    def unlock_normal(self, target):
        target = pm.PyNode(target)
        if target.getShape().nodeType() == 'mesh':
            self.poly_soft_edge(target, 0)
            self.poly_soft_edge(target, 1)

    def poly_soft_edge(self, target, ot=0): # ot (Operation Type), 0 = set to face, 1 = softenEdge
        node = None
        suffix = None
        target = pm.PyNode(target)
        target_shape_list = target.getShapes()

        old_node_list = self.list_connections(target, type = 'polySoftEdge')
        old_node_list.extend(self.list_connections(target, type = 'polyNormalPerVertex'))

        if ot == 0 :
            pm.polySetToFaceNormal(target)
            suffix = '_setNormal'
        elif ot == 1:
            pm.polySoftEdge(target, a = 180, ch = True)
            suffix = '_softEdge'

        new_node_list = self.list_connections(target, type = 'polySoftEdge')
        new_node_list.extend(self.list_connections(target, type = 'polyNormalPerVertex'))

        for new_node in new_node_list:
            if new_node not in old_node_list:
                node = new_node
            else:
                node = old_node_list[0]

        node.rename(target.stripNamespace() + suffix)
        return node

    def rename_tweak(self):
        tweak_list = pm.ls(type = 'tweak')

        type_list = ['mesh', 'nurbsCurve']

        for tweak in tweak_list:
            tfm_list = []
            for type in type_list:
                tfm_list.extend(tweak.listConnections(type = type))
            try:
                tfm = tfm_list[0]
                tweak.rename(tfm.nodeName() + '_tweak')
            except:
                print('... Cannot rename ' + tweak.nodeName())
    ##################
    ''' reorder  children '''
    ##################
    def reorder_children(self ,target):
        target = pm.PyNode(target)
        children_list = target.getChildren()
        children_list = self.natural_sort(children_list)
        for children in children_list[::-1]:
            pm.reorder(children, front = True)

    ##################
    ''' clean duplicate '''
    ##################
    def clean_duplicate(self, target, suffix='dup'):
        target = pm.PyNode(target)
        dup_target = pm.duplicate(target)[0]
        dup_target.rename(target.stripNamespace() + '_' + suffix)
        pm.parent(dup_target, world = True)
        self.lock_hide_attr(dup_target, en = False)
        self.freeze_transform(dup_target)
        self.center_pivot(dup_target)
        self.delete_history(dup_target)
        self.remove_from_all_set(dup_target)
        self.remove_from_all_layer(dup_target)
        self.empty_mesh_cache_name_attr(dup_target) # csMeshCache
        if target.getShapes():
            self.delete_non_visible_shape(dup_target)
            if target.getShape().nodeType() == 'mesh':
                pm.sets('initialShadingGroup', forceElement=dup_target)
        return(dup_target)

    # def copy_mesh_shape(self, driver, driven):
