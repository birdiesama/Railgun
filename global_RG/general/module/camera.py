################################################################################
__Script__		= 'global_RG.general.module.camera'
__Author__		= 'Weerapot Chaoman'
__Version__		= 3.00
__Date__		= 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import re
import pymel.core as pm
import pymel.core.uitypes as pmui
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
################################################################################

class Camera(object):

    def __init__(self, *args, **kwargs):

        super(Camera, self).__init__(*args, **kwargs)

        self.panel_attr_list = [ # last update: Maya 2018
            'controllers',
            'nurbsCurves',
            'nurbsSurfaces',
            'cv',
            'hulls',
            'polymeshes',
            'subdivSurfaces',
            'planes',
            'lights',
            'cameras',
            'imagePlane',
            'joints',
            'ikHandles',
            'deformers',
            'dynamics',
            'particleInstancers',
            'fluids',
            'hairSystems',
            'follicles',
            'nCloths',
            'nParticles',
            'nRigids',
            'dynamicConstraints',
            'locators',
            'dimensions',
            'pivots',
            'handles',
            'textures',
            'strokes',
            'motionTrails',
            'pluginShapes',
            'clipGhosts',
            'greasePencils',
            'pluginObjects',
            ]

    def get_active_cam(self):
        # return active current active viewport camera shape
        view = omui.M3dView.active3dView()
        cam = om.MDagPath()
        view.getCamera(cam)
        cam_path = cam.fullPathName()
        cam_node = pm.general.PyNode(cam_path)
        return cam_node

    def toggle_pan_zoom_lock(self):

        cam_node = self.get_active_cam()

        if pm.getAttr(cam_node.panZoomEnabled, lock = True):
            cam_node.panZoomEnabled.unlock() ;
            cam_node.panZoomEnabled.set(1) ;
            cam_node.horizontalPan.unlock() ;
            cam_node.verticalPan.unlock() ;
            cam_node.zoom.unlock() ;

        else:
            cam_node.panZoomEnabled.set(0) ;
            cam_node.panZoomEnabled.lock() ;
            cam_node.horizontalPan.lock() ;
            cam_node.verticalPan.lock() ;
            cam_node.zoom.lock() ;

    def toggle_resolution_gate(self):
        cam_node = self.get_active_cam()
        # set overscan to 1
        if cam_node.overscan.get() != 1:
            cam_node.overscan.unlock()
            pm.disconnectAttr(cam_node.overscan)
        # toggle
        status = pm.camera(cam_node.fullPath(), q = True, displayResolution = True)

        if not status :
            pm.camera(cam_node.fullPath(), e = True, displayFilmGate = False, displayResolution = True, overscan = 1.0, lockTransform = True)
        else :
            pm.camera(cam_node.fullPath(), e = True, displayFilmGate = False, displayResolution = False, overscan = 1.0, lockTransform = False)
        cam_node.displayGateMaskColor.set(0, 0, 0)
        cam_node.displayGateMaskOpacity.set(1)

    def toggle_anti_aliase(self):
        hardware_rendering_globals = pm.general.PyNode ('hardwareRenderingGlobals')
        if not hardware_rendering_globals.multiSampleEnable.get():
            hardware_rendering_globals.multiSampleEnable.set(1)
            hardware_rendering_globals.multiSampleCount.set(16)
        else:
            hardware_rendering_globals.multiSampleEnable.set(0)

    def toggle_viewport_renderer(self):
        model_panel_list = []
        editor_list = pm.lsUI(editors = True)

        active_model_editor_list = []
        for model_editor in editor_list:
            if 'modelPanel' in model_editor:
                if model_editor.getActiveView():
                    active_model_editor_list.append(model_editor)

        for active_model_editor in active_model_editor_list:
            if active_model_editor.getRendererName() == 'base_OpenGL_Renderer':
                active_model_editor.setRendererName('vp2Renderer')
            elif active_model_editor.getRendererName() == 'vp2Renderer':
                active_model_editor.setRendererName('base_OpenGL_Renderer')
            else:
                active_model_editor.setRendererName('vp2Renderer')

    ##################
    ''' Panel '''
    ##################

    def get_active_panel(self):
        active_panel = pm.getPanel(wf = True)
        if 'modelPanel' not in active_panel:
            active_panel =  'modelPanel4'
        return active_panel

    def get_panel_active_attr(self, panel):
        active_attr_list = []
        for attr in self.panel_attr_list:
            try:
                cmd = 'status = pm.modelEditor("{panel}", q = True, {attr} = True)'.format(panel = panel, attr = attr)
                exec(cmd)
                if status:
                    active_attr_list.append(attr)
            except:
                pass
        return active_attr_list

    def set_panel_attr(self, panel, attr_list, enable=True):

        if not isinstance(attr_list, list):
            attr_list = [attr_list]

        for attr in attr_list:
            print(attr, panel, enable)
            try:
                cmd = 'pm.modelEditor("{panel}", e = True, {attr} = {enable})'.format(panel = panel, attr = attr, enable = enable)
                print(cmd)
                exec(cmd)
                print(cmd)
            except:
                pass

    def panel_show_all(self, panel):
        pm.modelEditor(panel, e = True, allObjects = True)

    def panel_show_none(self, panel):
        pm.modelEditor(panel, e = True, allObjects = False)
