import sys

mp = r'D:\Dropbox\Script\PycharmProjects\Railgun'

if not mp in sys.path:
	sys.path.insert(0, mp)

# import utils_SP.quickGui.core as quickGui
# reload(quickGui)
# quickGui.run()


import global_RG.general.core as test
reload(test)
print test
for each in dir(test):
	print('- {0}'.format(each))