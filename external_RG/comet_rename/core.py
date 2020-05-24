import os
import pymel.core as pm
################################################################################
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

def run():
	comet_rename_file_path = __self_path__  + 'cometRename.txt'
	comet_rename_file = open(comet_rename_file_path, 'r')
	comet_rename_txt = comet_rename_file.read()
	comet_rename_file.close()
	pm.mel.eval(comet_rename_txt)
	pm.mel.eval('cometRename;')