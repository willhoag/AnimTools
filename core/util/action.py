import maya.cmds as cmds
import maya.mel as mel
from wh.util.lists import forceList


# for frame in ActionFrames()
    # for object in ActionNodes()
        # for attr in ActionAttrs()

# made this, but pymel probably as a better option for a superclass. Or maybe this should subclass one of those pymel classes then. Should look into that.

# ---------------------------------
# TIME CLASSES
# ---------------------------------

class ActionRange(object):

    """docstring for ActionRange"""

    def __init__(self, frameRange=None):
        super(ActionRange, self).__init__()

        self.highlighted = False

        if frameRange:

            playBackRange = {}
            playBackRange['start'] = int(frameRange[0])
            playBackRange['end'] = int(frameRange[1])

            self.range = playBackRange

        else:
            self.range = self.getActionFrameRange()

    def getActionFrameRange(self):

        playBackRange = {}

        playBackSlider = mel.eval('$tmp=$gPlayBackSlider')
        highlighted = cmds.timeControl(playBackSlider, q=True, rangeVisible=True)

        if highlighted:

            self.highlighted = True

            frameRange = cmds.timeControl(playBackSlider, q=True, rangeArray=True)

            playBackRange['start'] = int(frameRange[0])
            playBackRange['end'] = int(frameRange[1])

        else:

            playBackRange['start'] = int(cmds.playbackOptions(q=True, min=True))
            playBackRange['end'] = int(cmds.playbackOptions(q=True, max=True))

        return playBackRange


class ActionFrames(ActionRange):
    """docstring for ActionFrames"""
    def __init__(self, frameRange=None, step=1, single=False):
        super(ActionFrames, self).__init__(frameRange=frameRange)

        self.step = step

        if single and not self.highlighted:
            self.range = self.getCurrentTime()

        self.frames = range(self.range['start'], self.range['end'] + 1, self.step)

    def getCurrentTime(self):
        cFrame = int(cmds.currentTime(q=True))
        return {'start': cFrame, 'end': cFrame}

    def __iter__(self):

        return iter(self.frames)


# ---------------------------------
# NODE CLASSES
# ---------------------------------

# Here I need an ActonNode class to fill the ActionNodes class
# ActionNode will create an object with ActionAttrs in it.
# Then I'll be able to do:


class ActionNodes(object):

    """docstring for ActionNodes"""

    def __init__(self, nodes=None):
        super(ActionNodes, self).__init__()

        # Should find a better way to do this instead of using forceList
        if nodes:
            self.nodes = forceList(nodes)
        else:
            self.nodes = forceList(cmds.ls(sl=True))

    def __iter__(self):
        return iter(self.nodes)


class ActionAttrs(object):

    """docstring for ActionAttrs"""

    def __init__(self, node, attrs=None):
        super(ActionAttrs, self).__init__()

        self.node = node

        if attrs:
            self.attrs = attrs
        else:
            self.attrs = self.getActionAttrs()

    def __iter__(self):
        try:
            return iter(self.attrs)
        except TypeError:
            return iter([])

    def getActionAttrs(self):

        attrs = self.getSelected()

        if not attrs:
            attrs = self.getSettable()

        return attrs

    def getSelected(self):
        return cmds.channelBox('mainChannelBox', q=True, selectedMainAttributes=True)

    # keyable and unlocked only
    def getSettable(self):
        return cmds.listAttr(self.node, k=True, u=True)


class ActionKeyFrames(ActionRange, ActionNodes):

    """docstring for ActionKeyFrames"""

    def __init__(self, nodes=None, frameRange=None):
        ActionRange.__init__(self, frameRange=frameRange)
        ActionNodes.__init__(self, nodes=nodes)

        # Gather up all the keyframes for all the nodes
        keys = []
        for node in self.nodes:
            nodeKeys = cmds.keyframe(node, t=(self.range['start'], self.range['end']), q=True)
            if nodeKeys:
                keys += nodeKeys

        # Store keyframes with no duplicates
        self.keys = map(int, set(keys))

    def __iter__(self):

        return iter(self.keys)


# ---------------------------------
# CURVE CLASSES
# ---------------------------------

class ActionCurves(object):
    """docstring for ActionCurves"""
    def __init__(self, curves=None):
        super(ActionCurves, self).__init__()

        if not curves:
            curves = cmds.keyframe(q=True, selected=True, name=True)

        self.curves = curves

    def __iter__(self):
        return iter(self.curves)


# I should make this inherit from ActionCurves and have it iterate through curve and keys at the same time
class ActionKeys(object):
    """docstring for ActionKeys"""
    def __init__(self, curve, keys=None):
        super(ActionKeys, self).__init__()

        if not keys:
            keys = cmds.keyframe(curve, q=True, selected=True, indexValue=True)

        self.curve = curve
        self.keys = keys

    def __iter__(self):
        return iter(self.keys)


