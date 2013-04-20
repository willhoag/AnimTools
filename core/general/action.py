import maya.cmds as cmds
import maya.mel as mel


# for frame in ActionFrames()
    # for object in ActionObjects()
        # for channel in ActionChannels()

# made this, but pymel probably as a better option for a superclass. Or maybe this should subclass one of those pymel classes then. Should look into that.
class Channels(object):
    """docstring for Channels"""
    def __init__(self, node):
        super(Channels, self).__init__()
        self.node = node

    def getSelected(self):

        return cmds.channelBox('mainChannelBox', q=True, selectedMainAttributes=True)

    def getSettable(self, incStatics=True):

        if not incStatics:
            # keyable and unlocked only
            return cmds.listAttr(self.node, k=True, u=True)
        else:
            # all settable attrs in the channelBox
            return self.getChannelBoxAttrs(self.node, asDict=False, incLocked=False)

    def getChannelBoxAttrs(self, asDict=True, incLocked=True):

        statusDict = {}
        statusDict['keyable'] = cmds.listAttr(self.node, k=True, u=True)
        statusDict['locked'] = cmds.listAttr(self.node, k=True, l=True)
        statusDict['nonKeyable'] = cmds.listAttr(self.node, cb=True)

        if asDict:
            return statusDict
        else:
            attrs = []
            if statusDict['keyable']:
                attrs.extend(statusDict['keyable'])
            if statusDict['nonKeyable']:
                attrs.extend(statusDict['nonKeyable'])
            if incLocked and statusDict['locked']:
                attrs.extend(statusDict['locked'])
            return attrs


class ActionRange(object):
    """docstring for ActionRange"""
    def __init__(self, frameRange=None):
        super(ActionRange, self).__init__()

        if frameRange:

            playBackRange = {}
            playBackRange['start'] = int(frameRange[0])
            playBackRange['end'] = int(frameRange[1])

            self.range = playBackRange

        else:

            self.range = self.getActionFrameRange()

    # Should be seperated as a base class for ActionFrames and ActionKeyFrames
    def getActionFrameRange(self):

        playBackRange = {}

        playBackSlider = mel.eval('$tmp=$gPlayBackSlider')
        highlighted = cmds.timeControl(playBackSlider, q=True, rangeVisible=True)

        if highlighted:

            frameRange = cmds.timeControl(playBackSlider, q=True, rangeArray=True)

            playBackRange['start'] = int(frameRange[0])
            playBackRange['end'] = int(frameRange[1])

        else:

            playBackRange['start'] = int(cmds.playbackOptions(q=True, min=True))
            playBackRange['end'] = int(cmds.playbackOptions(q=True, max=True))

        return playBackRange


class ActionChannels(Channels):
    """docstring for ActionChannels"""
    def __init__(self, node, channels=None):
        super(ActionChannels, self).__init__(node)

        self.node = node

        if channels:
            self.channels = channels
        else:
            self.channels = self.getActionChannels(node)

    def __iter__(self):
        return iter(self.channels)

    def getActionChannels(self, node):

        if node:

            channels = self.getSelected()

            if not channels:
                channels = self.getSettable(node=self.node)

            return channels


class ActionObjects(object):
    """docstring for ActionObjects"""
    def __init__(self, nodes=None):
        super(ActionObjects, self).__init__()

        if nodes:
            self.nodes = forceList(nodes)
        else:
            self.nodes = forceList(cmds.ls(sl=True))

    def __iter__(self):
        return iter(self.nodes)


class ActionFrames(ActionRange):
    """docstring for actionFrames"""
    def __init__(self, frameRange=None, step=1):
        super(ActionFrames, self).__init__(frameRange=frameRange)

        self.step = step

    def __iter__(self):

        return iter(range(self.range['start'], self.range['end'] + 1, self.step))


class ActionKeyFrames(ActionRange):
    """docstring for ActionKeyFrames"""
    def __init__(self, nodes, frameRange=None):
        super(ActionKeyFrames, self).__init__(frameRange=frameRange)

        # Specified nodes, otherwise selected nodes
        self.nodes = ActionObjects(nodes=nodes)

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


# Should find a better way to do this.
# Also, move to utilities folder b/c it's not maya dependent
def forceList(var):

    if type(var) is not list:
            var = [var]
    return var
