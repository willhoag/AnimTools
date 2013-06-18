import maya.cmds as cmds
import maya.mel as mel


# from functools import wraps

def operateOnSelectedDecorator(fn):

    # @wraps  # So decorated functions have correct __name__ and __doc__ etc
    # Getting an error right now using this.

    def wrapper(*args, **kwargs):
        selection = cmds.ls(sl=True)
        return fn(selection, *args, **kwargs)

    return wrapper


class SuspendRefresh(object):

    def __enter__(self):
        cmds.refresh(suspend=True)

    def __exit__(self, *exc_info):
        cmds.refresh(suspend=False)


def suspendRefreshDecorator(fn):

    # @wraps

    def wrapper(*args, **kwargs):
        with SuspendRefresh():
            return fn(*args, **kwargs)

    return wrapper


# Need to break this up into separate decorators
class RestoreContext(object):

    def __init__(self):
        self.autoKeyState = None
        self.time = None
        self.selection = None

    def __enter__(self):
        self.autoKeyState = cmds.autoKeyframe(query=True, state=True)
        self.time = int(cmds.currentTime(q=True))
        self.selection = cmds.ls(sl=True)

    def __exit__(self, *exc_info):

        cmds.autoKeyframe(state=self.autoKeyState)
        cmds.currentTime(self.time)

        if self.selection:
            cmds.select(self.selection)


def restoreContextDecorator(fn):

    # @wraps

    def wrapper(*args, **kwargs):
        with RestoreContext():
            return fn(*args, **kwargs)

    return wrapper


class UndoChunk(object):

    def __enter__(self):
        cmds.undoInfo(openChunk=True)

    def __exit__(self, *exc_info):
        cmds.undoInfo(closeChunk=True)


def undoChunkDecorator(fn):

    # @wraps

    def wrapper(*args, **kwargs):
        with UndoChunk():
            return fn(*args, **kwargs)

    return wrapper


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
