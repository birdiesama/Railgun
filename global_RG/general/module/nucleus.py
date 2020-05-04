################################################################################
__Script__		= 'global_RG.general.module.nucleus'
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
import re
################################################################################

class Nucleus(object):

    def __init__(self, *args, **kwargs):
        super(Nucleus, self).__init__(*args, **kwargs)

    def get_space_scale(self, target):
        y_val = pm.polyEvaluate(target, boundingBox = True)[1]
        height = ((y_val[0] - y_val[1]) ** 2) ** 0.5 # absolute value
        standard_height = 18.00 # 1/10 scale
        standard_space_scale = 0.1 # 1/10 scale
        comparison_val = height / standard_height
        comparison_list = list(str(comparison_val))

        replace = False
        number = None
        index = 0

        for comparison in comparison_list:
            if not replace:
                if comparison == '0' or comparison == '.':
                    pass
                else:
                    number = float(comparison)
                    replace = True
                    comparison_list[index] = '1'
                index += 1
            else:
                if comparison == '0' or comparison == '.':
                    pass;
                else:
                    comparison_list[index] = '0'
                index += 1

        comparison_val = ''
        for comparison in comparison_list:
            comparison_val += comparison
        comparison_val = float(comparison_val)
        if number >= 5:
            comparison_val *= 10
        space_scale = standard_space_scale / comparison_val

        return space_scale

    def make_nRigid(self, target): # obsolete
        target = pm.PyNode(target)
        pm.select(target)
        # Create nRigid
        nRigid_shape = pm.mel.eval('makeCollideNCloth')[0]
        nRigid_shape = pm.PyNode(nRigid_shape)
        nRigid = nRigid_shape.getParent()
        nRigid.rename(target.stripNamespace() + '_nRigid')
        # Set default Value
        nRigid_shape.thickness.set(0.1)
        nRigid_shape.friction.set(0.5)
        nRigid_shape.stickiness.set(0.01)
        nRigid_shape.trappedCheck.set(0)
        nRigid_shape.pushOutRadius.set(0)
        # Return
        return nRigid

    def create_nRigid(self, target, parent=None): # current

        target = pm.PyNode(target)
        pm.select(target)

        # Create nRigid
        nRigid_shape = pm.mel.eval('makeCollideNCloth')[0]
        nRigid_shape = pm.PyNode(nRigid_shape)
        nRigid = nRigid_shape.getParent()
        nRigid.rename(target.stripNamespace() + '_nRigid')

        # Set default Value
        nRigid_shape.thickness.set(0.01)
        nRigid_shape.friction.set(0.5)
        nRigid_shape.stickiness.set(0.01)
        nRigid_shape.trappedCheck.set(0)
        nRigid_shape.pushOutRadius.set(0)

        if parent:
            pm.parent(nRigid, parent)

        # Return
        return nRigid

    def create_nCloth(self, target, parent=None):

        target = pm.PyNode(target)

        cloth_input_shape = self.get_visible_shape(target)

        shape_list = target.getShapes()
        for shape in shape_list:
            if shape != cloth_input_shape:
                pm.delete(shape)

        pm.select(target)
        nCloth_shape = pm.mel.eval('createNCloth 0;')[0]
        nCloth_shape = pm.PyNode(nCloth_shape)
        pm.select(clear = True)

        nCloth = nCloth_shape.getParent()
        nCloth.rename(target.nodeName() + '_nCloth')

        shape_list = target.getShapes()
        for shape in shape_list:
            if shape != cloth_input_shape:
                cloth_current_shape = shape
                cloth_current_shape.rename(target.nodeName() + '_outputClothShape')

        nCloth_shape.thickness.set(0.01)
        nCloth_shape.selfCollideWidthScale.set(3)
        nCloth_shape.collisionFlag.set(2)
        nCloth_shape.selfCollisionFlag.set(1)
        nCloth_shape.friction.set(0)
        nCloth_shape.stickiness.set(0)
        nCloth_shape.stretchResistance.set(120)
        nCloth_shape.compressionResistance.set(25)
        nCloth_shape.bendResistance.set(0.125)
        nCloth_shape.damp.set(0.25)
        nCloth_shape.scalingRelation.set(1)

        return(nCloth, nCloth_shape, [cloth_input_shape, cloth_current_shape])

    def get_object_from_nucleus(self, nucleus, type='nCloth'):
        nucleus = pm.PyNode(nucleus)
        object_list = nucleus.listHistory(nucleus, future=True, type=type)
        return object_list

    def get_sim_object_from_nucleus(self, nucleus_list):

        if not isinstance(nucleus_list, list):
            nucleus_list = [nucleus_list]

        sim_object_tfm_list = []

        for nucleus in nucleus_list:
            nucleus = pm.PyNode(nucleus)

            nCloth_list = self.get_object_from_nucleus(nucleus, type='nCloth')
            nCloth_tfm_list = pm.listRelatives(nCloth_list, parent=True)

            hairSystem_list = self.get_object_from_nucleus(nucleus, type='hairSystem')
            # hairSystem_tfm_list = pm.listRelatives(hairSystem_list, parent = True)

            sim_object_tfm_list.extend(nCloth_tfm_list)
            sim_object_tfm_list.extend(hairSystem_list)

        return sim_object_tfm_list

    def get_node(self, target_list, node_type=None):
        if not isinstance(target_list, list):
            target_list = [target_list]
        node_list = []
        for target in target_list:
            target = pm.PyNode(target)
            node = None
            if target.nodeType() == node_type:
                node = target
            elif self.get_visible_shape(target):
                target_shape = self.get_visible_shape(target)
                if target_shape:
                    if target_shape.nodeType() == node_type:
                        node = target_shape
                    else:
                        connection_list = pm.listConnections(target_shape, type = node_type, shapes = True)
                        connection_list = list(set(connection_list))
                        if connection_list:
                            node = connection_list
                        elif not connection_list:
                            if node_type == 'nCloth':
                                history_list = pm.listHistory(target_shape, type = node_type)
                                history_list = list(set(history_list))
                                if history_list:
                                    node = history_list

            if node:
                if isinstance(node, list):
                    node_list.extend(node)
                else:
                    node_list.append(node)

        node_list = list(set(node_list))
        return node_list

    def get_nucleus(self, target_list):
        nucleus_list = self.get_node(target_list, node_type='nucleus')
        return nucleus_list

    def get_nCloth_node(self, target_list):
        nCloth_list = self.get_node(target_list, node_type='nCloth')
        return nCloth_list

    def get_nRigid_node(self, target_list):
        nRigid_list = self.get_node(target_list, node_type='nRigid')
        return nRigid_list

    def get_hairSystem_node(self, target_list):
        hairSystem_list = self.get_node(target_list, node_type='hairSystem')
        return hairSystem_list

    def get_dynamicConstraint_node(self, target_list):
        dynamicConstraint_list = self.get_node(target_list, node_type='dynamicConstraint')
        return dynamicConstraint_list

    def get_nNode(self, target_list):

        level1_nNodeType_list = ['nRigid', 'hairSystem', 'dynamicConstraint']
        level2_nNodeType_list = ['nCloth']

        nNode_list = []

        for nNodeType in level1_nNodeType_list:
            nNode_list.extend(self.get_node(target_list, node_type = nNodeType))

        if not nNode_list:
            for nNodeType in level2_nNodeType_list:
                nNode_list.extend(self.get_node(target_list, node_type = nNodeType))

        return nNode_list

    def get_nucleus_from_members(self, target_list):
        nucleus_list = []
        nNode_list = self.get_nNode(target_list)
        if nNode_list:
            for nNode in nNode_list:
                nucleus_list.extend(nNode.listHistory(type='nucleus'))
        nucleus_list = list(set(nucleus_list))
        return nucleus_list

    def toggle_nObject_enable(self, target_list, enable=True):

        if not isinstance(target_list, list):
            target_list = [target_list]

        nucleus_list = self.get_nucleus(target_list)
        if nucleus_list:
            for nucleus in nucleus_list:
                try:
                    nucleus.enable.set(enable)
                except:
                    pm.warning('... {nucleus}.enable cannot be set, please check'.format(nucleus = nucleus.nodeName()))

        nCloth_list = self.get_nCloth_node(target_list)
        if nCloth_list:
            for nCloth in nCloth_list:
                try:
                    nCloth.isDynamic.set(enable)
                except:
                    pm.warning('... {nCloth}.isDynamic cannot be set, please check'.format(nCloth = nCloth.nodeName()))

        nRigid_list = self.get_nRigid_node(target_list)
        if nRigid_list:
            for nRigid in nRigid_list:
                try:
                    nRigid.isDynamic.set(enable)
                except:
                    pm.warning('... {nRigid}.isDynamic cannot be set, please check'.format(nRigid = nRigid.nodeName()))

        dynCon_list = self.get_dynamicConstraint_node(target_list)
        if dynCon_list:
            for dynCon in dynCon_list:
                try:
                    dynCon.enable.set(enable)
                except:
                    pm.warning('... {dynCon}.enable cannot be set, please check'.format(dynCon = dynCon.nodeName()))

        hairSystem_list = self.get_hairSystem_node(target_list)
        if hairSystem_list:
            for hairSystem in hairSystem_list:
                if enable:
                    simulation_method = 3
                else:
                    simulation_method = 0
                try:
                    hairSystem.simulationMethod.set(simulation_method)
                except:
                    pm.warning('... {hairSystem}.simulationMethod cannot be set, please check'.format(hairSystem = hairSystem.nodeName()))

    ##################
    ''' nCache '''
    ##################

    def nCache_get_data_path(self):
        scene_path = pm.system.sceneName()
        scene_name = os.path.basename(scene_path)
        workspace = pm.workspace(q = True, dir = True)

        if not scene_name:
            pm.error('... !! Please save your scene first before continuing')

        sub_path = scene_name.split('.')[0].split('__')
        sub_path = sub_path[-2] + '/' + sub_path[-1]

        path = workspace
        if '/maya/scenes/' in path:
            path = path.split('/maya/scenes/')[0]
        path += '/data/caches/nCache/'
        path += sub_path + '/'
        return path

    def nCache_create(self, target_list, substep=1):

        if not isinstance(target_list, list):
            target_list = [target_list]

        all_nucleus_list = pm.ls(type = 'nucleus')
        for nucleus in all_nucleus_list:
            nucleus.enable.set(0)

        nCache_nucleus_list = self.get_nucleus_from_members(target_list)
        for nucleus in nCache_nucleus_list:
            nucleus.enable.set(1)

        try:
            mel_cmd = 'deleteCacheFile 2 { "delete", "" } ;'
            pm.mel.eval(mel_cmd);
        except:
            pass

        if target_list:
            cache_name = self.compose_camel_case(target_list[0].stripNamespace())
            if len(target_list) > 1:
                cache_name += '_to_'
                cache_name += self.compose_camel_case(target_list[-1].stripNamespace())

        cache_data_path = self.nCache_get_data_path()

        mel_cmd = 'doCreateNclothCache 5 { "2", "1", "10", "OneFilePerFrame", "1", '
        mel_cmd += '"{cache_data_path}", '.format(cache_data_path = cache_data_path)
        mel_cmd += '"0", '
        mel_cmd += '"{cache_name}", '.format(cache_name = cache_name)
        mel_cmd += '"0", "add", "0", "%s", "1","0","1","mcx" } ;' % substep

        # Get panel active attr, show none
        active_panel = self.get_active_panel()
        panel_active_attr = self.get_panel_active_attr(panel = active_panel)
        self.panel_show_none(panel = active_panel)

        # Get rid of the annoying warning
        suppress_warning = pm.scriptEditorInfo(q = True, suppressWarnings = True)
        suppress_info = pm.scriptEditorInfo(q = True, suppressInfo = True)
        supress_errors = pm.scriptEditorInfo(q = True, suppressErrors = True)
        pm.scriptEditorInfo(suppressWarnings = True, suppressInfo = True, suppressErrors = True)

        # Begin simulation
        try:
            self.toggle_nObject_enable(target_list = target_list, enable = True)
            pm.mel.eval(mel_cmd)
        except:
            pm.warning('... Simulation did not start. Please check your nObject.')

        # Turn the warning back on
        pm.scriptEditorInfo(suppressWarnings = suppress_warning, suppressInfo = suppress_info, suppressErrors = supress_errors)
        for nucleus in nCache_nucleus_list:
            nucleus.enable.set(0)

        # Set the show panel to the initial state
        self.set_panel_attr(panel = active_panel, attr_list = panel_active_attr, enable = True)

    ##################
    ''' nConstraint '''
    ##################

    def is_nCon(self, target):
        target = pm.PyNode(target)
        try:
            return target.getShape().nodeType() == 'dynamicConstraint'
        except:
            return False

    def get_display_connections_stat(self, target):
        target = pm.PyNode(target)
        if self.is_nCon(target):
            return target.getShape().displayConnections.get()

    def toggle_nCon_display_connection(self, target, enable=True):
        target = pm.PyNode(target)
        if self.is_nCon(target):
            target_shape = target.getShape()
            target_shape.displayConnections.set(enable)

    def make_curves_dynamic(self, selection_list, attach_curve=True, snap_curve_base=False, collide_with_mesh=False, exact_shape_match=True):

        attach_curve = int(attach_curve)
        snap_curve_base = int(snap_curve_base)
        exact_shape_match = int(exact_shape_match)

        if len(selection_list) < 2:
            pass

        else:
            mesh_list = []
            crv_grp_list = []

            for selection in selection_list:
                if selection.nodeType() == 'mesh':
                    mesh_list.append(selection)
                elif selection.getShape():
                    if selection.getShape().nodeType() == 'mesh':
                        mesh_list.append(selection)
                else:
                    crv_grp_list.append(selection)

            if len(mesh_list) != 1:
                pass

            else:
                mesh = mesh_list[0]

                if mesh.nodeType() == 'mesh':
                    mesh_shape = mesh
                    mesh = mesh_shape.getParent()
                    mesh_shape_list = mesh.getShapes()
                else:
                    mesh = mesh
                    mesh_shape = self.get_visible_shape(mesh)
                    mesh_shape_list = mesh.getShapes()

                old_nRigid_list = pm.listConnections(mesh_shape_list, type = 'nRigid')
                old_outliner_obj_list = pm.ls(assemblies = True)

                pm.select(selection_list)
                cmd = 'makeCurvesDynamic 2 { "%d", "%d", "%d", "1", "0"};'%(attach_curve, snap_curve_base, exact_shape_match)
                pm.mel.eval(cmd)
                new_nRigid_list = pm.listConnections(mesh_shape_list, type = 'nRigid')
                new_outliner_obj_list = pm.ls(assemblies = True)

                for nRigid in new_nRigid_list:
                    if nRigid not in old_nRigid_list:
                        nRigid_shape = nRigid.getShape()
                        nRigid.rename(mesh.nodeName() + '_nRigid')
                        nRigid_shape.collide.set(collide_with_mesh)

                hair_system = None
                sim_crv_grp = None
                nRigid = None

                for obj in new_outliner_obj_list:
                    if obj not in old_outliner_obj_list:
                        shape = pm.listRelatives(obj, ad = True, shapes = True)[0]
                        if shape.nodeType() == 'hairSystem':
                            hair_system = obj
                        if shape.nodeType() == 'nurbsCurve':
                            sim_crv_grp = obj
                        if shape.nodeType() == 'nRigid':
                            nRigid = obj

                return(hair_system, nRigid, sim_crv_grp)
