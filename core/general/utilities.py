# Should be in a utiliteis folder. Might get rid of these b/c I dont' thnk I'm using them anymore.
# Integrated into class hierarchy. No need for these anymore.
import maya.cmds as cmds


def getSelectedChannels():
    '''
    return a list of attributes selected in the ChannelBox
    '''

    return cmds.channelBox('mainChannelBox', q=True, selectedMainAttributes=True)


def getChannelBoxAttrs(node=None, asDict=True, incLocked=True):
    '''
    return a dict of attributes in the ChannelBox by their status
    @param node: given node
    @param asDict:  True returns a dict with keys 'keyable','locked','nonKeyable' of attrs
                    False returns a list (non ordered) of all attrs available on the channelBox
    @param incLocked: True by default - whether to include locked channels in the return (only valid if not asDict)
    '''

    statusDict = {}
    if not node:
        node = cmds.ls(sl=True, l=True)[0]
    statusDict['keyable'] = cmds.listAttr(node, k=True, u=True)
    statusDict['locked'] = cmds.listAttr(node, k=True, l=True)
    statusDict['nonKeyable'] = cmds.listAttr(node, cb=True)
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


def getSettableChannels(node=None, incStatics=True):
    '''
    return a list of settable attributes on a given node
    @param node: node to inspect
    @param incStatics: whether to include non-keyable static channels (On by default)

    FIXME: BUG some Compund attrs such as constraints return invalid data for some of the
    base functions using this as they can't be simply set. Do we strip them here?
    ie: pointConstraint.target.targetWeight
    '''

    if not node:
        node = cmds.ls(sl=True, l=True)[0]

    if not incStatics:

        # keyable and unlocked only

        return cmds.listAttr(node, k=True, u=True)
    else:

        # all settable attrs in the channelBox

        return getChannelBoxAttrs(node, asDict=False, incLocked=False)


def getCurrentFrame():
    return int(cmds.currentTime(q=True))
