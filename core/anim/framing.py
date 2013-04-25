import maya.cmds as cmds
from wh.core.util.decorators import *


@skipUndoDecorator
@toggleScrubDecorator
def nextKey():
    cmds.currentTime(cmds.findKeyframe(timeSlider=1, which='next'), e=1)


@skipUndoDecorator
@toggleScrubDecorator
def previousKey():
    cmds.currentTime(cmds.findKeyframe(timeSlider=1, which='previous'), e=1)


@skipUndoDecorator
@toggleScrubDecorator
def nextFrame():
    cmds.currentTime(cmds.currentTime(q=1) + 1)


@skipUndoDecorator
@toggleScrubDecorator
def previousFrame():
    cmds.currentTime(cmds.currentTime(q=1) - 1)
