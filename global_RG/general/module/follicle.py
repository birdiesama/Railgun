################################################################################
__Script__		= 'global_RG.general.module.follicle'
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

class Follicle(object):

    def __init__(self, *args, **kwargs):
        super(Follicle, self).__init__(*args, **kwargs)

    def closest_point_on_mesh(self, mesh, pos):
        # return u_val, v_val
        mesh = pm.PyNode(mesh)
        mesh_shape = self.get_visible_shape(mesh)

        if mesh_shape.nodeType() == 'mesh':
            cpm = pm.createNode('closestPointOnMesh')
            mesh_shape.outMesh >> cpm.inMesh

            for axis, index in zip(['x', 'y', 'z'], [0, 1, 2]):
                pm.setAttr(cpm + '.inPosition' + axis.upper(), pos[index])

            u_val = cpm.result.parameterU.get()
            v_val = cpm.result.parameterV.get()

            pm.delete(cpm)

        return(u_val, v_val)

    def attach_fol_mesh(self, name, mesh, pos):

        mesh = pm.PyNode(mesh)
        mesh_shape = self.get_visible_shape(mesh)

        u_val, v_val = self.closest_point_on_mesh(mesh, pos)

        fol_shape = pm.createNode('follicle')
        fol = fol_shape.getParent()
        fol.rename(name)
        fol.simulationMethod.set(0)

        fol_shape.outRotate >> fol.r
        fol_shape.outTranslate >> fol.t

        mesh_shape.worldMatrix >> fol_shape.inputWorldMatrix
        mesh_shape.outMesh >> fol_shape.inputMesh
        # mesh.worldMatrix >> fol_shape.inputWorldMatrix
        # mesh.outMesh >> fol_shape.inputMesh
        fol_shape.parameterU.set(u_val)
        fol_shape.parameterV.set(v_val)
        return fol
