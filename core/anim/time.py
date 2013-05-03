import maya.cmds as cmds
from wh.core.util.decorators import *
from wh.core.util.action import ActionRange


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
    def prevKey(self):
        cmds.currentTime(cmds.findKeyframe(timeSlider=1, which='previous'), e=1)

    @skipUndoDecorator
    @toggleScrubDecorator
    def nextFrame(self):
        cmds.currentTime(cmds.currentTime(q=1) + 1)

    @skipUndoDecorator
    @toggleScrubDecorator
    def prevFrame(self):
        cmds.currentTime(cmds.currentTime(q=1) - 1)

    @skipUndoDecorator
    @toggleScrubDecorator
    def set(self, frame):
        cmds.currentTime(frame)

    def get(self):
        return int(cmds.currentTime(q=True))


# range=Range()
# range.setIn()
# range.setIn(frame=12)

class Range(object):

    """docstring for Range"""

    def __init__(self):
        super(Range, self).__init__()
        self.maxTime = cmds.playbackOptions(q=True, maxTime=True)
        self.minTime = cmds.playbackOptions(q=True, minTime=True)

    def set(self, range=None):

        if not range:
            range = ActionRange().range

        self.minTime = range['start']
        self.maxTime = range['end']

        cmds.playbackOptions(minTime=self.minTime, maxTime=self.maxTime)

    def setIn(self, frame=None):

        if not frame:
            frame = CurrentTime().get()

        range = {'start': frame, 'end': self.maxTime}

        self.set(range=range)

    def setOut(self, frame=None):

        if not frame:
            frame = CurrentTime().get()

        range = {'start': self.minTime, 'end': frame}

        self.set(range=range)

    def reset(self):

        range = {}

        range['start'] = cmds.playbackOptions(animationStartTime=True, q=True)
        range['end'] = cmds.playbackOptions(animationEndTime=True, q=True)

        self.set(range=range)
