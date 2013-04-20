import maya.cmds as cmds
import maya.mel as mel


class SkipUndo(object):

    def __enter__(self):
        cmds.undoInfo(swf=False)

    def __exit__(self, *exc_info):
        cmds.undoInfo(swf=True)


def skipUndoDecorator(fn):

    # @wraps

    def wrapper(*args, **kwargs):
        with SkipUndo():
            return fn(*args, **kwargs)

    return wrapper


class ToggleScrub(object):

    def __init__(self):
        self.playBackSlider = mel.eval('$tmp=$gPlayBackSlider')

    def __enter__(self):
        cmds.timeControl(self.playBackSlider, beginScrub=True, e=1)

    def __exit__(self, *exc_info):
        cmds.timeControl(self.playBackSlider, endScrub=True, e=1)


def toggleScrubDecorator(fn):

    # @wraps

    def wrapper(*args, **kwargs):
        with ToggleScrub():
            return fn(*args, **kwargs)

    return wrapper


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
