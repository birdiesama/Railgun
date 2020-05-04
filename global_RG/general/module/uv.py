################################################################################
__Script__		= 'global_RG.general.module.uv'
__Author__		= 'Weerapot Chaoman'
__Version__		= 1.31
__Date__		= 20200503
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import pymel.core as pm

class UV(object):

    def create_cfx_hair_uv(self, target_list):

        if not isinstance(target_list, list):
            target_list = [target_list]

        cfx_uv_name = 'cfx_hair_uv'
        create_uv = True

        for target in target_list:
            target = pm.PyNode(target)
            target_shape = self.get_visible_shape(target)

            uv_list = pm.polyUVSet(target, q = True, allUVSets = True)
            if uv_list:
                for uv in uv_list:
                    if uv == cfx_uv_name:
                        create_uv = False
            if create_uv:
                old_polyAutoProj_list = pm.listHistory(target_shape, type = 'polyAutoProj')
                pm.polyAutoProjection(target, createNewMap = True, uvSetName = cfx_uv_name, planes = 6, insertBeforeDeformers = True, layout = 2, name = target.nodeName() + '_papUV')
                pm.warning('CFX Hair UV set has been added to... ' + target.nodeName())
                pm.polyUVSet(uvSet = cfx_uv_name, currentUVSet = True)
                new_polyAutoProj_list = pm.listHistory(target_shape, type = 'polyAutoProj')
                for polyAutoProj in new_polyAutoProj_list:
                    if polyAutoProj not in old_polyAutoProj_list:
                        polyAutoProj.rename(target.nodeName() + '_autoUV')
