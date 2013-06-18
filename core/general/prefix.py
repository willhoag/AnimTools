import maya.cmds as cmds
from wh.core.general.shelf import makeShelfButton


def selectWithSelectedPrefix(suffixes, add=False):
    selection = cmds.ls(sl=True)
    pfxList = set()

    for s in selection:
        pfxList.add(getPrefix(s, '_'))

    if not add:
        cmds.select(clear=True)

    for pfx in pfxList:
        select = []

        for suffix in suffixes:
            select.append('_'.join([pfx, suffix]))

        cmds.select(select, add=True)


def reselectWithSelectedPrefix():
    selected = cmds.ls(sl=True)
    suffixes = set()
    for select in selected:
        suffixes.add(getSuffix(select, '_'))
    command = 'wh.selectWithSelectedPrefix(%s)' % suffixes
    makeShelfButton(command)


def getSuffix(string, split):
    suffix = split.join(string.split(split)[1:])
    return suffix


def getPrefix(string, split):
    prefix = string.split(split)[0]
    return prefix
