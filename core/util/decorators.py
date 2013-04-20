# Should be in a utilities folder

# import pymel.core as pm
import maya.cmds as cmds
# from functools import wraps


def operateOnSelectedDecorator(fn):

    # @wraps  # So decorated functions have correct __name__ and __doc__ etc

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


class RestoreContext(object):

    def __init__(self):
        self.autoKeyState = None
        self.timeStore = None
        self.selection = None

    def __enter__(self):
        self.autoKeyState = cmds.autoKeyframe(query=True, state=True)
        self.timeStore = cmds.currentTime(q=True)
        self.selection = cmds.ls(sl=True)

    def __exit__(self, *exc_info):

        cmds.autoKeyframe(state=self.autoKeyState)
        cmds.currentTime(self.timeStore)

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
