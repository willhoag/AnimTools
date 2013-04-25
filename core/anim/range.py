import maya.cmds as cmds
from wh.core.util.action import *

# range=Range()
# range.setIn()
# range.setIn(frame=12)


class Range(object):
    """docstring for Range"""
    def __init__(self):
        super(Range, self).__init__()
        self.maxTime = cmds.playbackOptions(q=True, maxTime=True)
        self.minTime = cmds.playbackOptions(q=True, minTime=True)

    def setRange(self, range=None):

        if not range:
            range = ActionRange().range

        self.minTime = range['start']
        self.maxTime = range['end']

        cmds.playbackOptions(minTime=self.minTime, maxTime=self.maxTime)

    def setIn(self, frame=None):

        if not frame:
            frame = self.getCurrentFrame()

        range = {'start': frame, 'end': self.maxTime}

        self.setRange(range=range)

    def setOut(self, frame=None):

        if not frame:
            frame = self.getCurrentFrame()

        range = {'start': self.minTime, 'end': frame}

        self.setRange(range=range)

    def reset(self):

        range = {}

        range['start'] = cmds.playbackOptions(animationStartTime=True, q=True)
        range['end'] = cmds.playbackOptions(animationEndTime=True, q=True)

        self.setRange(range=range)

    # Should factor this out to a super class or utility script
    def getCurrentFrame(self):
        return int(cmds.currentTime(q=True))
