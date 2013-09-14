import maya.cmds as cmds
import maya.mel as mel
from wh.util.strings import stripPrefix


def makeShelfButton(command, sourceType='python'):
    shelfLayout = mel.eval('string $temp = $gShelfTopLevel')
    shelf = cmds.tabLayout(shelfLayout, query=True, st=True)
    cmds.shelfButton(annotation='Saved selection',
                     image1='menuIconWindow.png', sourceType=sourceType,
                     command=command, parent=shelf)


# Custom Buttons
def reselect(add=False):
    selected = cmds.ls(sl=True)
    command = 'import maya.cmds as cmds\ncmds.select(%s, add=%s)' % (
        selected, add)
    makeShelfButton(command)


def reselectWithPrefixs(add=False):
    selection = cmds.ls(sl=True)
    names = []
    for select in selection:
        names.append(stripPrefix(select, '_'))
    import pdb
    pdb.set_trace()
    command = 'wh.selectWithPrefixs(%s, add=%s)' % (names, add)
    makeShelfButton(command)
