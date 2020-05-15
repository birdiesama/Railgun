import pymel.core as pm
import xgenm as xg
try:
    from csmaya.task.cfx.xgen.utils import import_xgen_build
except:
    pass

class XGen(object):

    def __init__(self):
        super(XGen, self).__init__()

    def importXGenRig(self, simRigNamespace):
        # return xGenRootNode ;
        # --> import xgen
        xGenRootNode = import_xgen_build(slot_name=simRigNamespace, namespace=simRigNamespace);
        xGenRootNode = pm.PyNode(xGenRootNode);

        xGenNamespace = xGenRootNode.namespace();
        xGenNamespace = xGenNamespace.strip(':');

        # --> meshCache
        # update_xgen_meshcache ( xGenNamespace , xGenRootNode.nodeName() ) ;

        csMeshProxy_list = pm.ls(type='csMeshProxy');

        for csMeshProxy in csMeshProxy_list:

            if csMeshProxy.namespace().strip(':') == simRigNamespace:
                driver = csMeshProxy;
            else:
                driven = csMeshProxy;

        driven.cachePath.unlock();
        driver.cachePath >> driven.cachePath;
        # disconnectAttr chr_granny1:slot.cs_meshcache_path chr_granny1:input_anim_meshcacheShape.cachePath;

        return ([xGenNamespace, xGenRootNode]);

    def guide_to_curve(self):
        selection_list = pm.ls(sl = True)
        curve_grp_list = []
        for selection in selection_list:
            pm.select(selection)
            curve_list = pm.mel.eval('xgmCreateCurvesFromGuides(0, 0)')
            curve_grp = pm.listRelatives(curve_list, parent = True)[0]
            curve_grp.rename(selection.nodeName() + '_GDC')
            pm.parent(curve_grp, w = True)
            curve_grp_list.append(curve_grp)
        return curve_grp_list

    def import_xgen_build_fromSlot(self):
        mesh_cache_list = pm.ls(sl = True)
        if not mesh_cache_list:
            mesh_cache_list = pm.ls(type = 'csMeshProxy')

        xGen_root_list = []
        for mesh_cache in mesh_cache_list:
            namespace = mesh_cache.namespace()
            namespace = namespace.strip(':')
            xGen_root = import_xgen_build(slot_name = namespace, namespace = namespace)
            xGen_root = pm.PyNode(xGen_root)
            xGen_root_list.append(xGen_root)
        return xGen_root_list
