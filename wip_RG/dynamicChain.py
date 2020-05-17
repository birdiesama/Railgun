import maya.cmds as cmds
import unittest
import MASH.api as mapi
reload(mapi)
import maya.mel as mel
import time
import MASH.dynamicsUtils as dynamics

cmds.file(force=True, new=True)

cmds.setAttr('persp.translateX', 53)
cmds.setAttr('persp.translateY', 26)
cmds.setAttr('persp.translateZ', 36)
cmds.setAttr('persp.rotateX', -30)
cmds.setAttr('persp.rotateY', 45)

cmds.polyTorus(r=2.5)

#create a new MASH network
mashNetwork = mapi.Network()
mashNetwork.createNetwork(name="DymamicsNetwork", geometry="Instancer")

cmds.setAttr( mashNetwork.distribute+".pointCount", 10)
cmds.setAttr( mashNetwork.distribute+".rotateX", 800)
cmds.setAttr( mashNetwork.distribute+".amplitudeX", 32)

dynamicsNode = mashNetwork.addNode("MASH_Dynamics")

channelRandom = mashNetwork.addChannelRandom(dynamicsNode)
cmds.setAttr( channelRandom.name+".dynamicsChannelName", 11)

falloff = channelRandom.addFalloff()
cmds.setAttr( falloff+".falloffShape", 2)
cmds.setAttr( falloff+".innerRadius", 1)


falloffParent = cmds.listRelatives(falloff, parent=True)[0]
cmds.setAttr( falloffParent+".translateX",15.8)
cmds.setAttr( falloffParent+".scaleX", 15)
cmds.setAttr( falloffParent+".scaleY", 15)
cmds.setAttr( falloffParent+".scaleZ", 15)

solver = cmds.ls(type="MASH_BulletSolver")[0]

#tell Maya to finish what it's doing before we continue
cmds.flushIdleQueue()

#playblast
cmds.playbackOptions( animationEndTime='5sec')
cmds.playblast(format="qt", viewer=True, p=100 )
