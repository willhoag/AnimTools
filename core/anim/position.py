import maya.cmds as cmds
from wh.core.general.context import *
from wh.core.general.action import *
import math
import maya.OpenMaya as om


# Per Frame
# Should be select n sources
@restoreContextDecorator
def rec(nodes=None):

    locs = []

    for node in ActionObjects(node=nodes):

        loc = matchLocator(node)
        locs.append(loc.name)

    return locs


class matchLocator(object):
    """docstring for posLocator"""
    def __init__(self, node):
        super(matchLocator, self).__init__()
        self.node = node
        self.name = self.makeLocator(self.node)
        snap(self.name, node)

    def makeLocator(self, node):
        # Make locator
        locName = '%s_posMatch' % node
        loc = cmds.spaceLocator(name=locName)[0]

        # Usint this until I can get snappng to work with different rotation orders.
        cmds.setAttr((loc + ".rotateOrder"), cmds.getAttr(node + ".rotateOrder"))

        # Make source Attr name
        locSourceAttrName = 'source'
        locNameAndAttr = '%s.%s' % (loc, locSourceAttrName)

        # Add and set soure attribute for reference later
        cmds.addAttr(loc, ln=locSourceAttrName, dt='string')
        cmds.setAttr(locNameAndAttr, node, lock=True, keyable=False, channelBox=False, typ='string')

        return loc


# For Range
# Should be select n sources

@suspendRefreshDecorator
@restoreContextDecorator
def recAnim(nodes=None, atKeys=False):

    locs = []
    aframes = ActionFrames()

    for node in ActionObjects(nodes=nodes):

        loc = rec([node])[0]

        if atKeys:
            aframes = ActionKeyFrames(node, [aframes.range['start'], aframes.range['end']])

        for frame in aframes:
            cmds.currentTime(frame)
            snap(loc, node)
            cmds.setKeyframe(loc)

        locs.append(loc)

    return locs


def snap(nodes=None, destination=None):

    nodes = ActionObjects(nodes=nodes)

    # Make last node the destination if one isn't specified
    if not destination:
        destination = nodes.nodes[-1]
        del nodes.nodes[-1]

    for node in nodes:
        snapTrans(node, destination)
        snapRots(node, destination)


def snapTrans(node, destination, x=True, y=True, z=True):
    translation = cmds.xform(destination, q=True, t=True, ws=True)
    cmds.xform(node, t=translation, ws=True)


def snapRots(node, destination, x=True, y=True, z=True):
    rotation = getWorldSpaceRotation(destination)
    cmds.xform(node, ro=rotation, ws=True)

# Scale?


def getWorldSpaceRotation(node):
    #-------------------------------------------
    # Part 1:  Get a MMatrix from an node

    # Not sure if this is getting the correct argument for eulerRot.reorderIt(rotOrder) down below
    # http://www.mail-archive.com/python_inside_maya@googlegroups.com/msg00740.html
    # http://forums.cgsociety.org/archive/index.php/t-1073798.html
    # http://www.akeric.com/blog/?p=1067
    rotOrder = cmds.getAttr('%s.rotateOrder' % node)

    # Get the world matrix as a list
    matrixList = cmds.getAttr('%s.worldMatrix' % node)  # len(matrixList) = 16
    # Create an empty MMatrix:
    mMatrix = om.MMatrix()  # MMatrix
    # And populate the MMatrix node with the matrix list data:
    om.MScriptUtil.createMatrixFromList(matrixList, mMatrix)

    #-------------------------------------------
    # Part 2, get the euler values
    # Convert to MTransformationMatrix to extract rotations:
    mTransformMtx = om.MTransformationMatrix(mMatrix)
    # Get an MEulerRotation node
    eulerRot = mTransformMtx.eulerRotation()  # MEulerRotation
    # Update rotate order to match original node, since the orig MMatrix has
    # no knoweldge of it:
    eulerRot.reorderIt(rotOrder)

    # Convert from radians to degrees:
    angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
    return angles


# Should be a select n sources then 1 destination for an x --> y (last is destination)
# Should be select 1 source/destination for an x --> x
# Should snap all x --> x with no input

@suspendRefreshDecorator
@restoreContextDecorator
def snapAnim(nodes=None, destination=None, atKeys=False):

    nodes = ActionObjects(nodes=nodes)

    if not destination:
        destination = nodes.nodes[-1]
        del nodes.nodes[-1]

    aframes = ActionFrames()

    for node in nodes:

        if atKeys:
            aframes = ActionKeyFrames(node, [aframes.range['start'], aframes.range['end']])

        for frame in aframes:
            cmds.currentTime(frame)
            snap(node, destination)
            cmds.setKeyframe(node)


# Should be a select n sources then 1 destination for an x --> y (last is destination)
# Should be select 1 source/destination for an x --> x
# Should snap all x --> x with no input

# DOESN'T WORK WITH CERTAIN CONSTRAINT HIERARCHIES!!! JUST RECORDING I THINK. ANYTHING THAT'S IN WS ALREADY WORKS GREAT AND IT CAN SNAP TO WS FROM ANYWHERE, BUT GETTING WS FROM SOME DOESN'T ALWAYS WORK. NEED TO IMPLEMENT ANOTHER METHOD. MAYBE DELETED CONSTRAINTS??? MATRIX MODE

# Todo:
# Need to make each one account for multiple nodes
# Need to name locators appropriately
# Need to consider alternitive to locators
# Need to make sure source gets keyed when snapping
# Need to make sure it maintains  selection

# Extra:
# Need to make at keys option or every frame
# Need to make range selective
# Need to find a way to iterate through frames faster
# Need to make option for do rotation translation or both. Maybe even a scale option
# Need to make Par and base controls for COG

# x=match(selected, position)
# x=match(selected, animation)
# x=match(selected, cog)
# x.snap
# x.snap(source, destination)

# x=match(selected) # creates match nodes
# x.recPosition
# x.recAnimation
# x.setupCog
# x.snapPosition
# x.snapAnimation
# x.snapAllCog

# x=matchPosition(selected)
# x=matchAnimation(selected)
# x=cog(selected)
# x.record
# x.snap

# x=match(selected, position)
# x=match(selected, animation)
# x=cog(selected)
# x.record
# x.snap
