################################################################################
__Script__		= 'global_RG.general.module.deformer'
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

class Deformer(object):

    def __init__(self):
        super(Deformer, self).__init__()

    def create_wrap(self, driver, driven):
        driver = pm.PyNode(driver)
        driver_shape = self.get_visible_shape(driver)
        driver_shape_list = driver.getShapes()

        mesh_shape_list = pm.listRelatives(driven, ad = True, type = 'mesh')
        mesh_list = pm.listRelatives(mesh_shape_list, parent = True)
        driven_list = mesh_list

        final_wrap_list = []
        final_wrap_base_list =[]

        for driven in driven_list:
            driven_shape = self.get_visible_shape(driven)
            driven_shape_list = driven.getShapes()

            old_wrap_list = []
            for shape in driven_shape_list:
                old_wrap_list.extend(shape.listConnections(type = 'wrap'))
            old_wrap_list = list(set(old_wrap_list))

            initial_component_list = [driver, driven]
            initial_component_list.extend(driver.getShapes())
            initial_component_list.extend(driven.getShapes())
            initial_component_list = list(set(initial_component_list))

            pm.select(driven, driver)
            pm.mel.eval('CreateWrap;')

            new_wrap_list = []
            for shape in driven_shape_list:
                new_wrap_list.extend(shape.listConnections(type = 'wrap'))
            new_wrap_list = list(set(new_wrap_list))

            wrap_list = []
            for new_wrap in new_wrap_list:
                if new_wrap not in old_wrap_list:
                    wrap_list.append(new_wrap)

            for wrap in wrap_list:
                wrap.rename(self.compose_camel_case(driver.nodeName()) + '_' + self.compose_camel_case(driven.nodeName()) + '_wrap')
                wrap.exclusiveBind.set(1)

            # wrap = wrap_list[0]
            wrap_connection_list = wrap.listConnections(wrap_list, type = 'mesh')
            wrap_connection_list = list(set(wrap_connection_list))

            wrap_base_list = []
            for connection in wrap_connection_list:
                if connection not in initial_component_list:
                    wrap_base_list.append(connection)

            if wrap_base_list:
                for wrap_base in wrap_base_list:
                    if wrap_base.nodeType() == 'mesh':
                        wrap_base = wrap_base.getParent()
                    wrap_base.rename(self.compose_camel_case(driver.nodeName()) + '_' + self.compose_camel_case(driven.nodeName()) + '_wrapBase')

            final_wrap_list.extend(wrap_list)
            final_wrap_base_list.extend(wrap_base_list)

        return final_wrap_list, final_wrap_base_list

    ######### BLENDSHAPE #########

    def quick_blendshape(self, driver, driven, name=None, prefix=False, suffix=True):

        if prefix:
            suffix = False

        driver = pm.PyNode(driver)
        driven = pm.PyNode(driven)
        # driven_shape = driven.getShape()

        target_shape_list = []
        type_list = ['mesh', 'nurbsCurve']
        for type in type_list:
            shape_list = driven.listRelatives(ad=True, type=type)
            target_shape_list.extend(shape_list)
        target_shape_list = list(set(target_shape_list))
        for target_shape in target_shape_list:
            if target_shape.isIntermediate():
                target_shape_list.remove(target_shape)

        # tweak node
        old_tweak_list = []
        if target_shape_list:
            for target_shape in target_shape_list:
                tweak_list = target_shape.listConnections(type='tweak')
                tweak_list = list(set(tweak_list))
                old_tweak_list.extend(tweak_list)

        # blend shape history
        blendshape_history_list = []

        for target_shape in target_shape_list:
            blendshape_history = target_shape.listHistory(type='blendShape', lv=1)
            if blendshape_history:
                blendshape_history_list.append([target_shape, blendshape_history[0]])

        blendshape = pm.blendShape(driver, driven, origin='world', automatic=True, weight=[0, 1], envelope=1)[0]

        # tweak node
        new_tweak_list = []
        if target_shape_list:
            for target_shape in target_shape_list:
                tweak_list = target_shape.listConnections(type='tweak')
                tweak_list = list(set(tweak_list))
                new_tweak_list.extend(tweak_list)
            if new_tweak_list:
                for new_tweak in new_tweak_list:
                    if new_tweak not in old_tweak_list:
                        pm.delete(new_tweak)

        # blend shape history
        if blendshape_history_list:
            for blendshape_history in blendshape_history_list:
                pm.reorderDeformers(blendshape, blendshape_history[1], blendshape_history[0])

        if name:
            blendshape.rename(name)
        else:
            name = self.compose_camel_case(driver.nodeName())
            if suffix:
                blendshape.rename(name + '_src_bsn')
            if prefix:
                blendshape.rename('BSH_src_{0}'.format(name))

        return blendshape

    def get_blendshape_member(self, blendshape_list, type = None):
        if not isinstance(blendshape_list, list):
            blendshape_list = [blendshape_list]
        return_list = []
        for blendshape in blendshape_list:
            blendshape = pm.PyNode(blendshape)
            set = blendshape.listConnections(type = 'objectSet')
            set_member_list = pm.sets(set, q = True)
            if type:
                set_member_list = pm.ls(set_member_list, o = True, type = type)
            else:
                set_member_list = pm.ls(set_member_list, o = True)
            return_list.extend(set_member_list)
        return return_list

    def blendshape_get_weight(self, mesh_shape, blendshape):
        mesh_shape = pm.PyNode(mesh_shape)
        blendshape = pm.PyNode(blendshape)
        vertex_no = pm.polyEvaluate(mesh_shape, vertex = True)
        # bsn_base_weight = list(blendshape.inputTarget[0].baseWeights.get())
        bsn_base_weight = mc.getAttr('{0}.inputTarget[0].baseWeights[0:{1}]'.format(blendshape, vertex_no))
        # bsn_iTarget_weight = list(blendshape.inputTarget[0].inputTargetGroup[0].targetWeights.get())
        bsn_iTarget_weight = mc.getAttr('{0}.inputTarget[0].inputTargetGroup[0].targetWeights[0:{1}]'.format(blendshape, vertex_no))
        return(bsn_base_weight, bsn_iTarget_weight, vertex_no)

    def blendshape_set_weight(self, mesh_shape, blendshape, bsn_base_weight, bsn_iTarget_weight, src_vertex_no):
        mesh_shape = pm.PyNode(mesh_shape)
        blendshape = pm.PyNode(blendshape)
        vertex_no = pm.polyEvaluate(mesh_shape, vertex = True)
        if src_vertex_no != vertex_no:
            pm.warning('... Source total vertices and target total vertices not match, you might get unexpected result')
        if bsn_base_weight:
            pm.setAttr('{0}.inputTarget[0].baseWeights[0:{1}]'.format(blendshape, vertex_no), *bsn_base_weight, size = len(bsn_base_weight))
        if bsn_iTarget_weight:
            pm.setAttr('{0}.inputTarget[0].inputTargetGroup[0].targetWeights[0:{1}]'.format(blendshape, vertex_no, *bsn_iTarget_weight, size = len(bsn_iTarget_weight)))
