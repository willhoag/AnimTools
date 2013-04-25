# import pymel.core as pm
import maya.cmds as cmds

# Should figure out a better way of doing this one:
from wh.core.util.decorators import *
from wh.core.util.action import *


class Keys(object):
    """For manipulating key values"""
    def __init__(self):
        super(Keys, self).__init__()
        self.pivotValue

    def scale():
        pass

    def contract():
        pass

    def exaggurate():
        pass

    def dampen():
        pass

    def copy():
        pass

    def flip():
        pass


# KeyFrame().initialize()

class KeyFrame(object):
    """For manipulating KeyFrames"""
    def __init__(self, frame=None, nodes=None, attrs=None):
        super(KeyFrame, self).__init__()

        if not frame:
            frame = self.getCurrentFrame

        self.frame = frame
        self.nodes = ActionNodes(nodes=nodes)
        self.attrs = attrs

    # Should factor this out to a super class or utility script - current duplicate in range.py
    def getCurrentFrame(self):
        return int(cmds.currentTime(q=True))

    @undoChunkDecorator
    def breakdown(percent=50):

        currentFrame = self.getCurrentFrame()

        for node in self.nodes:
            for channel in ActionAttrs(node, attrs=self.attrs):

                attr = node + '.' + channel
                nextKey = int(cmds.findKeyframe(node, t=(currentFrame, currentFrame), at=channel, which='next'))
                prevKey = int(cmds.findKeyframe(node, t=(currentFrame, currentFrame), at=channel, which='previous'))

                if not nextKey:
                    nextKey = currentFrame

                if not prevKey:
                    prevKey = currentFrame

                nextKeyValue = cmds.keyframe(attr, t=(nextKey, nextKey), q=True, ev=True)[0]
                prevKeyValue = cmds.keyframe(attr, t=(prevKey, prevKey), q=True, ev=True)[0]
                difference = nextKeyValue - prevKeyValue
                newValue = difference * percent * .01 + prevKeyValue
                cmds.setAttr(attr, newValue, c=True)

    @undoChunkDecorator
    def initialize():

        for node in self.nodes:
            for channel in ActionAttrs(node, attrs=self.attrs):

                defaultValue = cmds.attributeQuery(channel, node=str(node), ld=1)
                cmds.setAttr(str(node) + '.' + str(channel), defaultValue[0])


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
                for channel in ActionAttrs(node, attrs=self.attrs):

                    cmds.currentTime(frame)
                    cmds.setKeyframe(node, at=channel)

    @undoChunkDecorator
    @suspendRefreshDecorator
    @restoreContextDecorator
    def merge(self):

        for frame in ActionKeyFrames(self.nodes, frameRange=self.frames):
            cmds.currentTime(frame)
            cmds.setKeyframe()
