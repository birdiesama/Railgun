################################################################################
__Script__      = 'global_RG.general.module.alembic'
__Author__      = 'Weerapot Chaoman'
__Version__     = 1.01
__Date__        = 20191026
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

import pymel.core as pm

class Alembic(object):

    def __init__(self, *args, **kwargs):
        super(Alembic, self).__init__(*args, **kwargs)

    def alembic_export(self, target, path, name, frame_range=(950, 1200)):

        target = pm.PyNode(target)
        root = target.fullPath()

        start, end = frame_range

        if path[-1] != '/':
            path += '/'

        cmd = 'AbcExport -j '
        cmd += '"'
        cmd += '-frameRange {start} {end} '.format(start = start, end = end)
        cmd += '-uvWrite '
        cmd += '-worldSpace '
        cmd += '-writeVisibility '
        cmd += '-dataFormat ogawa '
        cmd += '-root {root} '.format(root = root)
        cmd += '-file {path}{name}.abc'.format(path = path, name = name)
        cmd += '";'
        pm.mel.eval(cmd)

### test
# abc = Alembic()
# abc.alembic_export(
#     target = '|op1:slot|op1:rig|op1:OUTPUT_SIM_GRP|op1:output_xGen_publish_grp',
#     frame_range = (1001, 1086),
#     path = '/vdisk/XTC/1200/0180/hairsim/work_wchaoman/workspace/maya/cache/alembic/op',
#     name = 'v007_001_headHair_tail')

'''
#   AbcExport -j"-frameRange 1001 1086-uvWrite-worldSpace-writeVisibility-dataFormat ogawa-root |op1:slot|op1:rig|op1:OUTPUT_SIM_GRP|op1:output_xGen_publish_grp-file /vdisk/XTC/1200/0180/hairsim/work_wchaoman/workspace/maya/cache/alembic/op/v007_001_headHair_tail.abc"; #
AbcExport -j "-frameRange 1001 1086 -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -root |op1:slot|op1:rig|op1:OUTPUT_SIM_GRP|op1:output_xGen_publish_grp -file /vdisk/XTC/1200/0180/hairsim/work_wchaoman/workspace/maya/cache/alembic/op/v007_001_headHair_tail.abc";
'''

'''
cmds.scriptEditorInfo(suppressWarnings=0,suppressInfo=0,se=0)
'''
# suppress_warning = pm.scriptEditorInfo(q = True, suppressWarnings = True)
# suppress_info = pm.scriptEditorInfo(q = True, suppressInfo = True)
# supress_errors = pm.scriptEditorInfo(q = True, suppressErrors = True)
