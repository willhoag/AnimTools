# import pymel.core as pm
import maya.cmds as cmds

# Should figure out a better way of doing this one:
from wh.core.util.decorators import *
from wh.core.util.action import *


class Keys(object):
    """For manipulating key values"""
    def __init__(self):
        super(Keys, self).__init__()

        if not pivotValue:
            pivotValue = cmds.keyframe(q=True, valueChange=True, lastSelected=True)[0]

        self.factor = factor
        self.individual = individual
        self.pivot = pivot
        self.pivotValue = pivotValue

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

    def iterate(fn):

        def wrapper(pivot=None, factor=1, pivotValue=None, individual=True):

            for curve in ActionCurves():

                if individual:
                    self.setPivotValueCurve(curve)

                for key in ActionKeys(curve):
                    return fn(self)

        return wrapper

    @iterate
    def push(self):
        cmds.scaleKey(curve, index=key, valuePivot=self.pivotValue, valueScale=True / self.factor)

    @iterate
    def pull(self):
        cmds.scaleKey(curve, index=key, valuePivot=self.pivotValue, valueScale=self.factor)

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
    def __init__(self, frames=None, nodes=None, attrs=None):
        super(KeyFrame, self).__init__()

        if not frames:
            frames = ActionFrames(single=True)

        self.frames = frames
        self.nodes = ActionNodes(nodes=nodes)
        self.attrs = attrs

    # Currently doesn't key unless the value changes...
    @undoChunkDecorator
    def breakdown(percent=50):

        for node in self.nodes:
            for attr in ActionAttrs(node, attrs=self.attrs):
                for frame in self.frames:

                    attr = node + '.' + attr
                    nextKey = int(cmds.findKeyframe(node, t=(frame, frame), at=attr, which='next'))
                    prevKey = int(cmds.findKeyframe(node, t=(frame, frame), at=attr, which='previous'))

                    if not nextKey:
                        nextKey = frame

                    if not prevKey:
                        prevKey = frame

                    nextKeyValue = cmds.keyframe(attr, t=(nextKey, nextKey), q=True, ev=True)[0]
                    prevKeyValue = cmds.keyframe(attr, t=(prevKey, prevKey), q=True, ev=True)[0]
                    difference = nextKeyValue - prevKeyValue
                    newValue = difference * percent * .01 + prevKeyValue
                    cmds.setAttr(attr, newValue, c=True)

    # Currently doesn't key unless the value changes...
    # Currently doesn't work for multiple frames
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
