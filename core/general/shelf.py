import maya.cmds as cmds
import maya.mel as mel


def reselect():
    selected = cmds.ls(sl=True)
    command = 'import maya.cmds as cmds\ncmds.select(%s, add=True)' % selected
    makeShelfButton(command)


def makeShelfButton(command):
    shelfLayout = mel.eval('string $temp = $gShelfTopLevel')
    shelf = cmds.tabLayout(shelfLayout, query=True, st=True)
    cmds.shelfButton(annotation='Saved selection',
                     image1='menuIconWindow.png', sourceType='python',
                     command=command, parent=shelf)
