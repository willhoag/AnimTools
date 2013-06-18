import maya.cmds as cmds
import maya.mel as mel
from wh.core.anim.position import SnapObject
from wh.core.util.decorators import *


# class camera
# Camera().follow()
@restoreContextDecorator
def followCam(name):
    parent = cmds.ls(sl=True)[0]
    focusedPanel = str(cmds.getPanel(withFocus=True))
    currentCam = str(cmds.modelPanel(focusedPanel, q=1, camera=1))

    aStr = []
    perspCenterOfInterest = float(cmds.camera(currentCam, q=1, coi=1))

    aStr = cmds.camera(coi=perspCenterOfInterest)

    drop = aStr[0]
    dropShape = aStr[1]

    camGrp = str(cmds.group(drop, n=(name + "Grp#")))

    cmds.makeIdentity(camGrp, apply=False, s=1, r=1, t=1)

    SnapObject(camGrp).snap(currentCam)

    cmds.parentConstraint(camGrp, mo=parent)

    # factor this out
    cmds.setAttr((camGrp + ".tx"), lock=True)
    cmds.setAttr((camGrp + ".ty"), lock=True)
    cmds.setAttr((camGrp + ".tz"), lock=True)
    cmds.setAttr((camGrp + ".rx"), lock=True)
    cmds.setAttr((camGrp + ".ry"), lock=True)
    cmds.setAttr((camGrp + ".rz"), lock=True)
    cmds.setAttr((camGrp + ".sx"), lock=True, channelBox=False, keyable=False)
    cmds.setAttr((camGrp + ".sy"), lock=True, channelBox=False, keyable=False)
    cmds.setAttr((camGrp + ".sz"), lock=True, channelBox=False, keyable=False)
    cmds.setAttr((drop + ".tx"), lock=True)
    cmds.setAttr((drop + ".ty"), lock=True)
    cmds.setAttr((drop + ".tz"), lock=True)
    cmds.setAttr((drop + ".rx"), lock=True)
    cmds.setAttr((drop + ".ry"), lock=True)
    cmds.setAttr((drop + ".rz"), lock=True)
    cmds.setAttr((drop + ".sx"), lock=True, channelBox=False, keyable=False)
    cmds.setAttr((drop + ".sy"), lock=True, channelBox=False, keyable=False)
    cmds.setAttr((drop + ".sz"), lock=True, channelBox=False, keyable=False)

    cmds.setAttr((dropShape + ".nearClipPlane"), 5)

    drop = str(cmds.rename(drop, (name + "#")))
    mel.lookThroughModelPanel(drop, focusedPanel)
