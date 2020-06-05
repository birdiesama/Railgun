################################################################################
__Script__          = 'global_RG.general.module.text'
__Author__          = 'Weerapot Chaoman'
__Version__         = 1.0
__Date__            = 20200601
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

class Text(object):

	def __init__(self):
		super(Text, self).__init__()

	def text_write(self, path, string=None, mode='w+'):
		txt_file = open(path, mode)
		if string:
			if not isinstance(string, str):
				string = str(string)
			txt_file.write(string)
		txt_file.close()

	def text_read(self, path, mode='r'):
		if os.path.exists(path):
			txt_file = open(path, mode)
			txt_txt = txt_file.read()
			txt_file.close()
			return(txt_txt)
		else:
			return(None)