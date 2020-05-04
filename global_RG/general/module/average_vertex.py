################################################################################
__Script__		= 'global_RG.general.module.average_vertex'
__Author__		= 'Weerapot Chaoman'
__Version__		= 2.00
__Date__		= 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

import pymel.core as pm

class AverageVertex(object):

    def __init__(self):
        super(AverageVertex, self).__init__()

    def get_average_vertex(self, target):
        target = pm.PyNode(target)
        if hasattr(target, 'getShape'):
            target = target.getShape()
            # target = self.get_visible_shape(target)
        average_vertex_list = pm.listConnections(target, type = 'polyAverageVertex')
        average_vertex_list = list(set(average_vertex_list))
        return(average_vertex_list)
