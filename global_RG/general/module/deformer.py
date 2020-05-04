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
