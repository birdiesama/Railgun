################################################################################
__Script__          = 'global_RG.general.module.utils'
__Author__          = 'Weerapot Chaoman'
__Version__         = 1.0
__Date__            = 20200605
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import pymel.core as pm
import maya.cmds as mc
################################################################################

class Utils(object):

    def __init__(self):
        super(Utils, self).__init__()

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

    ######### Contraint #########

    def quick_par_con(self, driver, driven, mo=False, name=None):
        par_con = pm.parentConstraint(driver, driven, mo = mo, skipRotate = 'none', skipTranslate = 'none')
        if name:
            par_con.rename(name)
        else:
            par_con.rename(driven.stripNamespace() + '_parCon')
        return par_con

    def quick_point_con(self, driver, driven, mo=False, name=None):
        point_con = pm.pointConstraint(driver, driven, mo = mo, skip = 'none')
        if name:
            point_con.rename(name)
        else:
            point_con.rename(driven.stripNamespace() + '_pointCon')
        return point_con