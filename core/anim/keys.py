# import pymel.core as pm
import maya.cmds as cmds

# Should figure out a better way of doing this one:
from wh.core.util.decorators import *
from wh.core.util.action import *
from wh.core.anim.time import CurrentTime


class Keys(object):
    """For manipulating key values"""
    def __init__(self, pivot=None, scaleFactor=1, pivotValue=None, affect='individual'):
        super(Keys, self).__init__()

        if not pivotValue:
            pivotValue = cmds.keyframe(q=True, valueChange=True, lastSelected=True)[0]

        self.pivotValue = pivotValue
        self.scaleFactor = scaleFactor
        self.affect = affect

    def scale(self):
        pass

    def contract(self):
        pass

    def exaggurate(self):
        pass

    def dampen(self):
        pass

    def copy(self):
        pass

    def flip(self):
        pass

    def run(fn):

        def wrapper(*args, **kwargs):

            for curve in ActionCurves():

                self.setPivotValueCurve(curve)

                for key in ActionKeys(curve):
                    return fn(*args, **kwargs)

        return wrapper

    @run
    def push(self):
        cmds.scaleKey(curve, index=key, valuePivot=self.pivotValue, valueScale=True / self.scaleFactor)

    @run
    def pull(self):
        cmds.scaleKey(curve, index=key, valuePivot=self.pivotValue, valueScale=self.scaleFactor)

    def setPivotValueCurve(self, curve):

            timeArray = cmds.keyframe(curve, q=True, timeChange=True, selected=True)

            # per curve pivot value value
            if self.pivot == 'left':
                pivotTime = float(cmds.findKeyframe(curve, which='previous', time=timeArray[0]))
                self.pivotValue = cmds.keyframe(curve, q=True, valueChange=True, time=pivotTime)[0]

            if self.pivot == 'right':
                pivotTime = float(cmds.findKeyframe(curve, which='next', time=timeArray[-1]))
                self.pivotValue = cmds.keyframe(curve, q=True, valueChange=True, time=pivotTime)[0]


# KeyFrame().initialize()

class KeyFrame(object):
    """For manipulating KeyFrames"""
    def __init__(self, frame=None, nodes=None, attrs=None):
        super(KeyFrame, self).__init__()

        if not frame:
            frame = CurrentTime().get()

        self.frame = frame
        self.nodes = ActionNodes(nodes=nodes)
        self.attrs = attrs

    # Currently doesn't key unless the value changes...
    @undoChunkDecorator
    def breakdown(percent=50):

        for node in self.nodes:
            for attr in ActionAttrs(node, attrs=self.attrs):

                attr = node + '.' + attr
                nextKey = int(cmds.findKeyframe(node, t=(self.frame, self.frame), at=attr, which='next'))
                prevKey = int(cmds.findKeyframe(node, t=(self.frame, self.frame), at=attr, which='previous'))

                if not nextKey:
                    nextKey = self.frame

                if not prevKey:
                    prevKey = self.frame

                nextKeyValue = cmds.keyframe(attr, t=(nextKey, nextKey), q=True, ev=True)[0]
                prevKeyValue = cmds.keyframe(attr, t=(prevKey, prevKey), q=True, ev=True)[0]
                difference = nextKeyValue - prevKeyValue
                newValue = difference * percent * .01 + prevKeyValue
                cmds.setAttr(attr, newValue, c=True)

    # Currently doesn't key unless the value changes...
    @undoChunkDecorator
    def initialize():

        for node in self.nodes:
            for attr in ActionAttrs(node, attrs=self.attrs):

                defaultValue = cmds.attributeQuery(attr, node=str(node), ld=1)
                cmds.setAttr(str(node) + '.' + str(attr), defaultValue[0])


class KeyFrames(KeyFrame):
    """For manipulating KeyFrames"""
    def __init__(self, nodes=None, attrs=None, frameRange=None):
        super(KeyFrames, self).__init__(nodes=None, attrs=None)

        self.frames = ActionFrames(frameRange=frameRange)

    # Current implementation adjusts keys depending on tangent. Need alternative for this
    @undoChunkDecorator
    @suspendRefreshDecorator
    @restoreContextDecorator
    def bake(self):

        for frame in self.frames:
            for node in self.nodes:
                for attr in ActionAttrs(node, attrs=self.attrs):
                    cmds.setKeyframe(node, at=attr, t=[frame, frame])

    @undoChunkDecorator
    @suspendRefreshDecorator
    @restoreContextDecorator
    def merge(self):

        for frame in ActionKeyFrames(self.nodes, frameRange=self.frames):
            cmds.setKeyframe(t=[frame, frame])
