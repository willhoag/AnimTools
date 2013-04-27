# import pymel.core as pm
import maya.cmds as cmds

# Should figure out a better way of doing this one:
from wh.core.util.decorators import *
from wh.core.util.action import *
from wh.core.anim.frames import CurrentTime


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
            frame = CurrentTime().get()

        self.frame = frame
        self.nodes = ActionNodes(nodes=nodes)
        self.attrs = attrs

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

                    CurrentTime().set(frame)
                    cmds.setKeyframe(node, at=attr)

    @undoChunkDecorator
    @suspendRefreshDecorator
    @restoreContextDecorator
    def merge(self):

        for frame in ActionKeyFrames(self.nodes, frameRange=self.frames):
            CurrentTime().set(frame)
            cmds.setKeyframe()
