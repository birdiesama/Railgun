import os
import re

from maya import cmds, mel
import pymel.core as pm

try:
    import cs.pipeline as pipe
    import csmaya.core.render_globals.xml_utilities as xml
    import csmaya.task.lighting.utilities as ut
except:
    pass

class RenderGlobalsCopy(object):
    """
    :param str show:
    :param str scene:
    :param str shot:
    :param str renderer:
    :param str globals_node:
    :param str xml_file:
    :param dict[str, list[xml.AttributeObject]] layer_dict:
    :param dict[str, str] aov_dict:
    """

    def __init__(self, renderer='arnold'):
        super(RenderGlobalsCopy, self).__init__()
        """
        :param str renderer:
        """
        try:
            self.show = os.environ.get('SHOW')
            self.scene = os.environ.get('SCENE')
            self.shot = os.environ.get('SHOT')
            self.renderer = renderer
            self.globals_node = ut.get_globals_node_from_renderer(renderer)
            self.xml_file = self.get_config_file(self.show, self.renderer)
            self.layer_dict = xml.get_attributes_from_xml(self.xml_file)
            self.aov_dict = xml.get_aov_groups_from_xml(self.xml_file)
        except:
            pass

    @staticmethod
    def get_config_file(show='', renderer='arnold'):
        """
        Get the show specific render globals config file.

        :param str show: name of the show
        :param str renderer: name of the renderer

        :rtype: str
        """
        show = show or os.environ.get('SHOW', '')
        return '//vdisk/{}/config/applications/maya/{}/render_globals/render_globals.xml'.format(show, renderer)

    @staticmethod
    def isfloat(element):
        """
        Is the provided element convertible to a float.

        :param element:

        :rtype: bool
        """
        try:
            float(element)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_animation_range():
        """
        Get the animation range from Maya.

        :rtype: tuple[int, int]
        """
        return int(pm.playbackOptions(animationStartTime=True, q=True)), \
            int(pm.playbackOptions(animationEndTime=True, q=True))

    @staticmethod
    def get_playback_range():
        """
        Get the playback range from Maya.

        :rtype: tuple[int, int]
        """
        return int(pm.playbackOptions(minTime=True, q=True)), \
            int(pm.playbackOptions(maxTime=True, q=True))

    @staticmethod
    def get_global_range():
        """
        Get the defaultRenderGlobals range from Maya.

        :rtype: tuple[int, int]
        """
        return pm.getAttr('defaultRenderGlobals.startFrame'), \
            pm.getAttr('defaultRenderGlobals.endFrame')

    def get_frame_range(self):
        """
        Get the work frame range for the shot as found in Ftrack,
        if not found fallback on animation range.

        :rtype: tuple[float, float]
        :returns: a tuple of floats, 2 elements including start frame and end frame
        """
        shot = pipe.Shot()
        # if the shot has been tagged to work
        # to the preretime range use that
        try:
            if 'work_preretime' in shot.ftrack_handle.get('editorial_tags'):
                start_frame, end_frame = shot.preretime_frame_range
            else:
                # if not use pre retime use the standard time
                start_frame, end_frame = shot.work_frame_range
        except:
            pm.warning('Frame range cannot be found for the shot %s' % shot)
            start_frame, end_frame = self.get_animation_range()

        return float(start_frame), float(end_frame)

    def get_render_frame_range(self):
        """
        Get the lighting render frame range from FTrack,
        if not found  fallback on self.get_frame_range.

        :rtype: tuple[float, float]
        """
        try:
            # Getting lighting render ranges from ftrack if it has been added
            # Should be added as a default ftrack attribute for future shows
            shot = pipe.Shot()
            if not shot:
                raise KeyError
            start_frame, end_frame = shot.ftrack_handle.dict['lighting_render_range'].split('-')
        except KeyError:
            start_frame, end_frame = self.get_frame_range()

        return float(start_frame), float(end_frame)

    def set_frame_range(self, start_frame=None, end_frame=None, render_range=False):
        """
        Set the frame range for the shot
        - if start and end frame not specified default to what's found in FTrack.

        :param float start_frame:
        :param float end_frame:
        :param bool render_range:
        """
        if start_frame is None or end_frame is None:
            if render_range:
                start_frame, end_frame = self.get_render_frame_range()
            else:
                start_frame, end_frame = self.get_frame_range()

        pm.playbackOptions(minTime=start_frame, maxTime=end_frame,
                           animationStartTime=start_frame, animationEndTime=end_frame)
        node = pm.PyNode('defaultRenderGlobals')
        node.startFrame.set(start_frame)
        node.endFrame.set(end_frame)


def load_arnold_aovs(prefix='IMPORT', file_path=None, use_confirm_ui=False, replace_existing_aovs=True):
    """
    :param str prefix:
    :param str file_path:
    :param bool use_confirm_ui:
    :param bool replace_existing_aovs:
    """
    if use_confirm_ui:
        confirm = ut.confirm_ui('Do you want to load AOVs from the file:\n' + file_path)
    else:
        confirm = 'Yes'

    if confirm == 'Yes':
        if os.path.exists(file_path):
            print 'Loading Arnold AOVs from', file_path
            nodes = cmds.file(file_path, i=True, renameAll=True, renamingPrefix=prefix, returnNewNodes=True)
            for node in nodes:
                existing_node = node[len(prefix) + 1:]
                node_type = cmds.nodeType(node)
                if pm.objExists(existing_node) and node_type == 'aiAOV':
                    if replace_existing_aovs:
                        pm.delete(existing_node)
                        pm.rename(node, existing_node)
                    else:
                        pm.delete(node)
                else:
                    pm.rename(node, existing_node)

            # Connect up AOVs
            aov_nodes = pm.ls(type='aiAOV')

            if pm.objExists('defaultArnoldRenderOptions'):
                arnold_options = pm.PyNode('defaultArnoldRenderOptions')

                for aov in aov_nodes:
                    if not pm.connectionInfo(aov.message, dfs=True):
                        pm.connectAttr(aov + '.message', arnold_options.aovList.elementByLogicalIndex(arnold_options.aovList.getNumElements()))

            # Cleanup unconnected drivers and filters
            ai_nodes = pm.ls(type=['aiAOVDriver', 'aiAOVFilter'])
            for ai_node in ai_nodes:
                try:
                    attr = pm.PyNode(ai_node.longName() + '.message')
                except pm.MayaAttributeError:
                    continue
                outputs = attr.outputs()
                if not outputs:
                    pm.delete(ai_node)
        else:
            pm.warning(file_path, 'does not exist.')
