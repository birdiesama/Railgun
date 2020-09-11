################################################################################
__Script__		= 'global_RG.general.module.color'
__Author__		= 'Weerapot Chaoman'
__Version__		= 2.0
__Date__		= 20191212
################################################################################
import os, sys
import pymel.core as pm
from colorsys import rgb_to_hsv, hsv_to_rgb
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

class Color(object):

    def __init__(self, *args, **kwargs):

        super(Color, self).__init__(*args, **kwargs)

        self.color_rgb_dict = {}

        self.color_rgb_dict['blue']         = (0, 0, 1)
        self.color_rgb_dict['light_blue']   = (0, 0.8, 1)

        # self.color_rgb_dict['sea_green']    = (0.2, 0.55, 0.35)
        # self.color_rgb_dict['light_sea_green'] = (0.55, 0.75, 0.55)
        self.color_rgb_dict['sea_green']    = (0, 0.55, 0.55)
        self.color_rgb_dict['light_sea_green'] = (0, 0.75, 0.75)

        self.color_rgb_dict['green']        = (0, 1, 0)
        self.color_rgb_dict['light_green']  = (0.5, 1, 0.5)

        self.color_rgb_dict['yellow']       = (1, 1, 0)
        self.color_rgb_dict['light_yellow'] = (1, 1, 0.5)

        self.color_rgb_dict['orange']       = (1, 0.65, 0)
        self.color_rgb_dict['light_orange'] = (1, 0.6, 0.4)

        self.color_rgb_dict['red']          = (1, 0, 0)
        self.color_rgb_dict['light_red']    = (1, 0.25, 0.5)

        self.color_rgb_dict['brown']        = (0.6, 0.1, 0.1)
        self.color_rgb_dict['light_brown']  = (0.6, 0.3, 0.3)

        self.color_rgb_dict['purple']       = (0.6, 0, 0.8)
        self.color_rgb_dict['light_purple'] = (0.85, 0.6, 0.85)

        self.color_rgb_dict['pink']         = (1, 0.4, 0.7)
        self.color_rgb_dict['light_pink']   = (1, 0.7, 0.75)

        self.color_rgb_dict['skin']         = (1, 0.85, 0.75)
        self.color_rgb_dict['skin_light']   = (1, 0.9, 0.9)
        self.color_rgb_dict['skin_dark']    = (0.75, 0.55, 0.55)

        self.color_rgb_dict['black']        = (0, 0, 0)
        self.color_rgb_dict['dark_grey']    = (0.25, 0.25, 0.25)
        self.color_rgb_dict['grey']         = (0.5, 0.5, 0.5)
        self.color_rgb_dict['light_grey']   = (0.75, 0.75, 0.75)
        self.color_rgb_dict['white']        = (1, 1, 1)

    def get_rgb_complementary(self, rgb):
        r, g, b = rgb
        h, s, v = rgb_to_hsv(r, g, b)
        complementary = hsv_to_rgb((h + 0.5 % 1), s, v)
        return complementary

    def assign_poly_shader(self, target_list, color_name, transparency=None):

        if not transparency:
            transparency = 100

        shader_name = color_name + '_shader'
        shading_grp_name = shader_name

        if transparency:
            shader_name += '_{0}'.format(transparency)
            shading_grp_name += '_{0}'.format(transparency)

        shading_grp_name += 'SG'

        # check if shader exists
        if pm.objExists(shader_name):
            shader = pm.PyNode(shader_name)
            shading_grp = pm.PyNode(shading_grp_name)
        else:
            shader = pm.shadingNode('blinn', asShader = True, n = shader_name)
            for connection in shader.listConnections():
                if connection.nodeType() == 'shadingEngine':
                    pm.delete(connection)
            shading_grp = pm.sets(renderable = True, noSurfaceShader = True, em = True, n = shading_grp_name)
            shader.outColor >> shading_grp.surfaceShader
            shader.color.set(self.color_rgb_dict[color_name])
            shader.specularColor.set(0.15, 0.15, 0.15)
            shader.eccentricity.set(1.0)
            shader.specularRollOff.set(0.3)
            shader.reflectivity.set(0)

            transparency_val = 0
            if transparency:
                transparency_val = 1 - (transparency / 100.00)

            shader.transparency.set(transparency_val, transparency_val, transparency_val)

        # assign
        if not isinstance(target_list, list):
            target_list = [target_list]

        for target in target_list:
            pm.sets(shading_grp, e = True, forceElement = target)

    def assign_outliner_color(self, target_list, rgb=None, color_name=None, en=True):
        if not isinstance(target_list, list):
            target_list = [target_list]
        if not en:
            for target in target_list:
                target = pm.PyNode(target)
                target.useOutlinerColor.set(0)
        else:
            for target in target_list:
                target = pm.PyNode(target)
                target.useOutlinerColor.set(1)
                if rgb:
                    pass
                if color_name:
                    rgb = self.color_rgb_dict[color_name]
                target.outlinerColor.set(rgb)