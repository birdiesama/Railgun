import sys
import importlib

mp = r'C:\Users\birdi\Dropbox\Script\PycharmProjects\Railgun'

if not mp in sys.path:
	sys.path.insert(0, mp)

import global_RG.quick_gui.core as qgui
importlib.reload(qgui)
qgui.run()