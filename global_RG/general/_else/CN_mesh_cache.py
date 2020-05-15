################################################################################
__Script__		= 'utils_SP.general.mesh_cache'
__Author__		= 'Weerapot Chaoman'
__Version__		= 1.4
__Date__		= 20190806
__Location__	= 'Cinesite Montreal'
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Snowpiercer'
################################################################################

import pymel.core as pm

try:
    from csmaya.core.meshcache.outputs import createMeshes
except:
    pass

class MeshCache(object):
    # requires compose_name

    def __init__(self, *args, **kwargs):
        super(MeshCache, self).__init__(*args, **kwargs)

    def get_selected_csMesh(self):
        csMesh_proxy = pm.ls(sl=True)[0].listRelatives(type='csMeshProxy')
        if csMesh_proxy:
            return (pm.csMeshProxyCmd(csMesh_proxy, listSelection=True)[0], csMesh_proxy[0])

    def get_mesh_cache_connections(self, target):
        target = pm.PyNode(target)
        list__connection = target.listConnections(plugs = True, connections = True)
        list__return = []

        if list__connection:
            for connection in list__connection:
                source = connection[1]
                destination = connection[0].attrName()
                # check if the source node is csMeshCache
                if source.node().nodeType() == 'csMeshProxy':
                    list__return.append([source, destination])

        if not list__return:
            list__return = None

        return list__return

    def copy_meshcache_connections(self, mesh_src, mesh_des):

        mesh_src = pm.PyNode(mesh_src)
        mesh_des = pm.PyNode(mesh_des)

        list__mesh_cache_connection = self.get_mesh_cache_connections(mesh_src)

        if not list__mesh_cache_connection:
            pm.warning("... there's no csMeshCache connection to [{mesh_des}]".format(mesh_des = mesh_des))

        else:
            for connection in list__mesh_cache_connection:
                attr__source = pm.PyNode(connection[0])
                attr__destination = pm.PyNode(mesh_des.fullPath() + '.' + connection[1])
                attr__source >> attr__destination
                print("... {attr__source} >> {attr__destination}".format(attr__source = attr__source, attr__destination = attr__destination))

    def copy_selectedMesh_meshcache_connections(self):

        list_selection = pm.ls(sl=True)

        tfm_source = pm.PyNode(list_selection[0])
        tfm_destination = pm.PyNode(list_selection[1])

        list_meshShape_source = tfm_source.listRelatives(ad=True, type='mesh')
        list_mesh_source = pm.listRelatives(list_meshShape_source, parent=True)
        list_mesh_source = list(set(list_mesh_source))
        list_meshShape_source = []
        for mesh in list_mesh_source:
            list_meshShape_source.append(self.get_visible_shape(mesh))
        list_meshShape_source = self.natural_sort(list_meshShape_source)

        list_meshShape_destination = tfm_destination.listRelatives(ad=True, type='mesh')
        list_mesh_destination = pm.listRelatives(list_meshShape_destination, parent=True)
        list_mesh_destination = list(set(list_mesh_destination))
        list_meshShape_destination = []
        for mesh in list_mesh_destination:
            list_meshShape_destination.append(self.get_visible_shape(mesh))
        list_meshShape_destination = self.natural_sort(list_meshShape_destination)

        for source_shape, destination_shape in zip(list_meshShape_source, list_meshShape_destination):
            source = source_shape.getParent()
            destination = destination_shape.getParent()

            self.copy_meshcache_connections(source, destination)
            self.copy_meshcache_connections(source_shape, destination_shape)

    def create_selected_csMesh(self, csMesh_proxy, csMesh_path):
        csMesh_proxy = pm.PyNode(csMesh_proxy)
        createMeshes(csMesh_proxy, objects=str(csMesh_path), meshConnections=1, transformConnections=1)
        csMesh_proxy_tfm = csMesh_proxy.getParent()
        mesh_list = csMesh_proxy_tfm.listRelatives(ad=True, type='mesh')
        mesh_list = list(set(mesh_list))
        mesh = pm.listRelatives(mesh_list, parent=True)[0]
        residual = csMesh_proxy_tfm.listRelatives(type='transform')
        # pm.delete(residual)
        return mesh

    def quick_mesh_cache_extract(self):
        suffix_outProxy = '_outProxy'
        group_inputRig = 'input_rig_grp'
        group_outputHires = 'output_highRes_outProxy_grp'
        group_outputPublish = 'output_highRes_publish_grp'
        set_meshcache = 'meshcache_set'

        csMesh_path, csMesh_proxy = self.get_selected_csMesh()
        name_csMeshParent = csMesh_path.split('|')[-2]
        namespace = csMesh_proxy.namespace()

        # input_rig
        if pm.objExists(namespace + group_inputRig):
            group_inputRig = pm.PyNode(namespace + group_inputRig)
        else:
            group_inputRig = None
        group_inputRig_csMeshParent = None
        if group_inputRig:
            list_children_group_inputRig = group_inputRig.listRelatives(ad=True, type='transform')
            for children in list_children_group_inputRig:
                if children.nodeName() == namespace + name_csMeshParent:
                    group_inputRig_csMeshParent = pm.PyNode(children)
        if not group_inputRig_csMeshParent:
            if pm.objExists(namespace + str(group_inputRig) + '_proxy'):
                group_inputRig_csMeshParent = pm.PyNode(namespace + group_inputRig + '_proxy')
            else:
                group_inputRig_csMeshParent = pm.group(em=True, w=True, n=namespace + str(group_inputRig) + '_proxy')

        if pm.objExists(namespace + group_outputHires):
            group_outputHires = pm.PyNode(namespace + group_outputHires)
        else:
            if pm.objExists(namespace + group_outputHires + '_proxy'):
                group_outputHires = pm.PyNode(namespace + group_outputHires + '_proxy')
            else:
                group_outputHires = pm.group(em=True, w=True, n=namespace + group_outputHires + '_proxy')

        if pm.objExists(namespace + group_outputPublish):
            group_outputPublish = pm.PyNode(namespace + group_outputPublish)
        else:
            group_outputPublish = None
        group_outputPublish_csMeshParent = None
        if group_outputPublish:
            list_children_group_outputPublish = group_outputPublish.listRelatives(ad=True, type='transform')
            for children in list_children_group_outputPublish:
                if children.nodeName() == namespace + name_csMeshParent:
                    group_outputPublish_csMeshParent = pm.PyNode(children)
        if not group_outputPublish_csMeshParent:
            if pm.objExists(namespace + group_outputPublish + '_proxy'):
                group_outputPublish_csMeshParent = pm.PyNode(namespace + group_outputPublish + '_proxy')
            else:
                group_outputPublish_csMeshParent = pm.group(em=True, w=True,
                                                            n=namespace + group_outputPublish + '_proxy')

        mesh_input = self.create_selected_csMesh(csMesh_proxy, csMesh_path)
        pm.parent(mesh_input, group_inputRig_csMeshParent)
        mesh_input.rename(namespace + mesh_input.nodeName())

        mesh_outputHires = pm.duplicate(mesh_input)[0]
        pm.parent(mesh_outputHires, group_outputHires)
        mesh_outputHires.rename(namespace + mesh_input.nodeName() + '_outProxy')

        mesh_outputPublish = self.create_selected_csMesh(csMesh_proxy, csMesh_path)
        pm.parent(mesh_outputPublish, group_outputPublish_csMeshParent)
        mesh_outputPublish.rename(namespace + mesh_outputPublish.nodeName())

        self.quick_blendshape(mesh_input, mesh_outputHires)
        self.quick_blendshape(mesh_outputHires, mesh_outputPublish)

        # include into mesh cahce set
        if pm.objExists(namespace + 'meshcache_set'):
            pm.sets(namespace + 'meshcache_set', add=mesh_outputPublish)

    def empty_mesh_cache_name_attr(self, target_list):
        if not isinstance(target_list, list):
            target_list = [target_list]
        target_shape_list = pm.listRelatives(ad = True, shapes = True)
        for shape in target_shape_list:
            if pm.attributeQuery('meshcacheName', node = shape, exists = True):
                shape.meshcacheName.set('')

    def extract_geo_from_mesh_cache(self, mesh_cache_proxy=None, name=None, suffix=None, parent=None, specific_geo=None):

        # specific_geo = individual geo to extract

        if not specific_geo:

            if mesh_cache_proxy.nodeType() != 'csMeshProxy':
                mesh_cache_proxy = pm.listRelatives(mesh_cache_proxy, ad = True, type = 'csMeshProxy')[0]

            mesh_cache = mesh_cache_proxy.getParent()

            pm.select(mesh_cache)
            createMeshes(proxies = None, progress = True, meshConnections = True, transformConnections = True) # extract mesh cache

            extracted_top_node = mesh_cache.listRelatives(type = 'transform')
            # if len(extracted_top_node) > 1: # for VFX
            #     extracted_top_node = pm.group(em = True, w = True, name = 'mesh_cache')
            #     pm.parent(mesh_cache.listRelatives(type = 'transform'), extracted_top_node)
            # else:
            #     extracted_top_node = extracted_top_node[0]

            elem_list = []
            # elem_list.extend([['working', 'rig']]) # TAF
            elem_list.extend(['world_constr_GRP', 'world_offset_GRP']) # RD
            elem_list.extend(['rig_local_GRP', 'world__ZERO']) # Extinct

            for node in extracted_top_node:
                for elem in elem_list:
                    if node.nodeName() == elem:
                        node.v.set(False)
                for child in node.getChildren():
                    for elem in elem_list:
                        if child.nodeName() == elem:
                            child.v.set(False)
            if name:
                new_top_node = pm.group(em = True, name = name, w = True)
                pm.parent(extracted_top_node, new_top_node)
                extracted_top_node = [new_top_node]
            if suffix:
                for node in extracted_top_node:
                    for child in node.listRelatives(ad = True, type = 'transform'):
                        child.rename(child.nodeName() + '_' + suffix)
            if parent:
                pm.parent(extracted_top_node, parent)

            return(extracted_top_node)
