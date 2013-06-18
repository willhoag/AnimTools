import maya.cmds as cmds
from wh.core.util.decorators import *
from wh.core.util.action import ActionRange
import maya.mel as mel


# how do I get rid of all these decorators?
class CurrentTime(object):

    """docstring for Frame"""

    def __init__(self):
        super(CurrentTime, self).__init__()

    @staticmethod
    @skipUndoDecorator
    @toggleScrubDecorator
    def nextKey():
        cmds.currentTime(cmds.findKeyframe(timeSlider=1, which='next'), e=1)

    @staticmethod
    @skipUndoDecorator
    @toggleScrubDecorator
    def prevKey():
        cmds.currentTime(cmds.findKeyframe(timeSlider=1, which='previous'), e=1)

    @staticmethod
    @skipUndoDecorator
    @toggleScrubDecorator
    def nextFrame():
        cmds.currentTime(cmds.currentTime(q=1) + 1)

    @staticmethod
    @skipUndoDecorator
    @toggleScrubDecorator
    def prevFrame():
        cmds.currentTime(cmds.currentTime(q=1) - 1)

    # Can't get to play with sound
    @staticmethod
    @skipUndoDecorator
    @toggleScrubDecorator
    def play():
        mel.eval('playButtonForward;')
        #playBackSlider = mel.eval('$tmp=$gPlayBackSlider')
        #sound = cmds.timeControl(playBackSlider, query=True, sound=True)
        #cmds.play(forward=True, playSound=True, sound=sound)

    @staticmethod
    @skipUndoDecorator
    def stop():
        cmds.play(state=False)

    @staticmethod
    @skipUndoDecorator
    @toggleScrubDecorator
    def set(frame):
        cmds.currentTime(frame)

    @staticmethod
    def get():
        return int(cmds.currentTime(q=True))


# range=Range()
# range.setIn()
# range.setIn(frame=12)

class Time(object):
    """docstring for Time"""
    def __init__(self):
        super(Time, self).__init__()
        self.startTime = cmds.playbackOptions(animationStartTime=True, q=True)
        self.endTime = cmds.playbackOptions(animationEndTime=True, q=True)

    def set():
        pass


class Range(Time):

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

        range['start'] = self.startTime
        range['end'] = self.endTime

        self.set(range=range)


class AnimView(Range):
    """docstring for AnimView"""
    def __init__(self, bookends=2):
        super(AnimView, self).__init__()
        self.bookends = bookends

    def matchRange(self):
        cmds.animView(startTime=self.minTime - self.bookends, endTime=self.maxTime + self.bookends)

    def matchTime(self):
        cmds.animView(startTime=self.startTime - self.bookends, endTime=self.endTime + self.bookends)
