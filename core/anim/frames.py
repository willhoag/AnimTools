import maya.cmds as cmds
from wh.core.util.decorators import skipUndoDecorator, toggleScrubDecorator


class CurrentTime(object):

    """docstring for Frame"""

    def __init__(self):
        super(CurrentTime, self).__init__()

    @skipUndoDecorator
    @toggleScrubDecorator
    def nextKey(self):
        cmds.currentTime(cmds.findKeyframe(timeSlider=1, which='next'), e=1)

    @skipUndoDecorator
    @toggleScrubDecorator
    def previousKey(self):
        cmds.currentTime(cmds.findKeyframe(timeSlider=1, which='previous'), e=1)

    @skipUndoDecorator
    @toggleScrubDecorator
    def nextFrame(self):
        cmds.currentTime(cmds.currentTime(q=1) + 1)

    @skipUndoDecorator
    @toggleScrubDecorator
    def previousFrame(self):
        cmds.currentTime(cmds.currentTime(q=1) - 1)

    @skipUndoDecorator
    @toggleScrubDecorator
    def set(self, frame):
        cmds.currentTime(frame)

    def get(self):
        return int(cmds.currentTime(q=True))
