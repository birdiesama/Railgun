################################################################################
__Script__		= 'global_RG.general.module.soft_cluster'
__Author__		= 'Weerapot Chaoman'
__Version__		= 1.2
__Date__		= 20200503
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

import pymel.core as pm
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

class SoftCluster(object):

    def __init__(self, *args, **kwargs):
        super(SoftCluster, self).__init__(*args, **kwargs)

    def get_soft_selection_weight(self):
        ### modified from https://gist.github.com/jhoolmans/9195634

        selection = om.MSelectionList()
        soft_selection = om.MRichSelection()
        om.MGlobal.getRichSelection(soft_selection)
        soft_selection.getSelection(selection)

        dag_path = om.MDagPath()
        component = om.MObject()

        iter = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
        elements = []

        while not iter.isDone():
            iter.getDagPath(dag_path, component)
            dag_path.pop()
            node = pm.PyNode(dag_path.fullPathName())
            fnComp = om.MFnSingleIndexedComponent(component)

            for i in range(fnComp.elementCount()):
                elements.append([node, fnComp.element(i), fnComp.weight(i).influence()] )
            iter.next()

        return elements

    def create_soft_cluster(self):
        softElem = self.get_soft_selection_weight()
        soft_selection = pm.ls(sl = True)
        current_frame = str(int(pm.currentTime(q = True)))
        name =  'frame' + current_frame + '_sc'

        cluster_list = pm.cluster(soft_selection, name = name)
        clusterHandle = cluster_list[1]
        clusterNode = clusterHandle.listConnections(type = 'cluster')[0]
        clusterSet = clusterNode.listConnections(type = 'objectSet')[0]

        selection_shape_list = pm.ls(soft_selection, o = True)

        for selection_shape in selection_shape_list:
            pm.sets(clusterSet, add = selection_shape.nodeName() + '.vtx[*]') # Add all vertex to cluster set member
            pm.percent(clusterNode, selection_shape.nodeName() + '.vtx[*]',  v = 0) # Set all vertex cluster value to 0

            selection = ["%s.vtx[%d]" % (el[0], el[1])for el in softElem]

            for i in range(len(softElem)):
                pm.percent(clusterNode, selection[i], v=softElem[i][2])
                pm.select(clusterNode)

        pm.select(clusterHandle)

    def make_cluster_group(self, selection_list):
        current_frame = str(int(pm.currentTime(q = True)))
        group = pm.group(selection_list)
        group.rename('f{current_frame}_{index}'.format(current_frame = current_frame, index = '1'.zfill(3)))
        self.lock_hide_attr(group)

        group.addAttr('envelope', keyable = True, attributeType = 'float', max = 1, min = 0, dv = 1)
        for each in selection_list:
            connections = each.connections()
            for connection in connections:
                if connection.nodeType() == 'cluster':
                    connection = pm.general.PyNode(connection)
                    group.envelope >> connection.envelope
        return group
