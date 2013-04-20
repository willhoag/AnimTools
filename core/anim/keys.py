# import pymel.core as pm
import maya.cmds as cmds

# Should figure out a better way of doing this one:
from wh.core.general.utilities import getCurrentFrame
from wh.core.general.context import *
from wh.core.general.action import *


class Keys(object):
    """For manipulating key values"""
    def __init__(self):
        super(Keys, self).__init__()

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
    def __init__(self, nodes=None, channels=None):
        super(KeyFrames, self).__init__()

        self.nodes = ActionObjects(nodes=nodes)
        self.channels = channels

    @undoChunkDecorator
    def breakdown(percent=50):

        currentFrame = getCurrentFrame()

        for node in self.nodes:

            for channel in ActionChannels(node, channels=self.channels):

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

            for channel in ActionChannels(node, channels=self.channels):

                defaultValue = cmds.attributeQuery(channel, node=str(node), ld=1)
                cmds.setAttr(str(node) + '.' + str(channel), defaultValue[0])


class KeyFrames(KeyFrame):
    """For manipulating KeyFrames"""
    def __init__(self, nodes=None, channels=None):
        super(KeyFrames, self).__init__(nodes=None, channels=None)

        self.frames = ActionFrames(frameRange=frameRange)

    # Current implementation adjusts keys depending on tangent. Need alternative for this
    @undoChunkDecorator
    @suspendRefreshDecorator
    @restoreContextDecorator
    def bake(frameRange=None):

        for frame in self.frames:

            for node in self.nodes:

                for channel in ActionChannels(node, channels=self.channels):

                    cmds.currentTime(frame)
                    cmds.setKeyframe(node, at=channel)

    @undoChunkDecorator
    @suspendRefreshDecorator
    @restoreContextDecorator
    def merge(frameRange=None):

        for frame in ActionKeyFrames(self.nodes, frameRange=self.frames):
            cmds.currentTime(frame)
            cmds.setKeyframe()
