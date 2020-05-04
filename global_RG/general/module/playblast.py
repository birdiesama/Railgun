################################################################################
__Script__      = 'global_RG.general.module.playblast'
__Author__      = 'Weerapot Chaoman'
__Version__     = 2.00
__Date__        = 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import pymel.core as pm
################################################################################

# playblast  -format image -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 75 -compression "maya" -quality 70 -widthHeight 4448 3096;

import pymel.core as pm

class Playblast(object):

    def __init__(self):
        super(Playblast, self).__init__()

    def get_scene_resolution(self):
        width = pm.getAttr('defaultResolution.width')
        height = pm.getAttr('defaultResolution.height')
        return(width, height)

    # def tempt_playblast(self):
    #     start, end = self.get_render_frame_range()
    #     width, height = self.get_scene_resolution()
    #     pm.playblast(
    #         format          = 'image',
    #         startTime       = start,
    #         endTime         = end,
    #         sequenceTime    = 0,
    #         clearCache      = 1,
    #         viewer          = 1,
    #         showOrnaments   = 1,
    #         offScreen       = True,
    #         fp              = 4, # framePadding
    #         percent         = 100,
    #         compression     = 'maya',
    #         quality         = 100,
    #         widthHeight     = [width, height],
    #         )
