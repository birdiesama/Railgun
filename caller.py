import sys

mp = r'D:\Dropbox\Script\PycharmProjects\Railgun'

if not mp in sys.path:
	sys.path.insert(0, mp)

import global_RG.quick_gui.core as qgui
reload(qgui)
qgui.run()