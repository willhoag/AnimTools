import maya.cmds as cmds
from wh.core.util.decorators import suspendRefreshDecorator, restoreContextDecorator
from wh.core.util.action import *
from wh.core.anim.time import CurrentTime
import math
import maya.OpenMaya as om


class Transform(object):
    """Better name for this?"""
    def __init__(self, node):
        super(Transform, self).__init__()
        self.node = node

    def getWorldSpaceRotation(self):

        # Part 1:  Get a MMatrix from an object
        # You can use your own MMatrix if it already exists of course.

        # Get the self.node's rotate order value:
        rotOrder = cmds.getAttr('%s.rotateOrder' % self.node)
        # Get the world matrix as a list
        matrixList = cmds.getAttr('%s.worldMatrix' % self.node)  # len(matrixList) = 16
        # Create an empty MMatrix:
        mMatrix = om.MMatrix()  # MMatrix
        # And populate the MMatrix object with the matrix list data:
        om.MScriptUtil.createMatrixFromList(matrixList, mMatrix)

        # Part 2, get the euler values
        # Convert to MTransformationMatrix to extract rotations:
        mTransformMtx = om.MTransformationMatrix(mMatrix)
        # Get an MEulerRotation object
        eulerRot = mTransformMtx.eulerRotation()  # MEulerRotation
        # Update rotate order to match original object, since the orig MMatrix has
        # no knoweldge of it:
        eulerRot.reorderIt(rotOrder)

        # Convert from radians to degrees:
        angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
        return angles


# for node in ActionNodes()
#    SnapObject(node).snap(destination)

class SnapObject(Transform):
    """
    for node in ActionNodes()
        SnapObject(node).snap(destination)
    """
    def __init__(self, name):
        super(SnapObject, self).__init__(name)
        self.name = name

    def snap(self, destination):
        self.snapTrans(destination)
        self.snapRots(destination)

    # Would like to subdivide these into x, y, z
    def snapTrans(self, destination):
        translation = cmds.xform(destination, q=True, t=True, ws=True)
        cmds.xform(self.name, t=translation, ws=True)

    # Would like to subdivide these into x, y, z
    def snapRots(self, destination):
        rotation = Transform(destination).getWorldSpaceRotation()
        cmds.xform(self.name, ro=rotation, ws=True)

    @suspendRefreshDecorator
    @restoreContextDecorator
    def snapAnim(self, destination, atKeys=False):

        if atKeys:
            aframes = ActionKeyFrames(destination)
        else:
            aframes = ActionFrames()

        time = CurrentTime()

        for frame in aframes:
            time.set(frame)
            self.snap(destination)
            cmds.setKeyframe(self.name)


class MatchLocator(SnapObject):
    """
    for node in AcionNodes():
        MatchLocator(node).matchAnim(atKeys=True)
    """

    def __init__(self, source):
        super(MatchLocator, self).__init__(source)

        self.source = source
        self.makeLocator()
        self.match()

    @restoreContextDecorator
    def makeLocator(self):
        # Make locator
        locName = '%s_posMatch' % self.source
        self.name = cmds.spaceLocator(name=locName)[0]

        # Usint this until I can get snappng to work with different rotation orders.
        cmds.setAttr((self.name + ".rotateOrder"), cmds.getAttr(self.source + ".rotateOrder"))

        # Make source Attr name
        locSourceAttrName = 'source'
        locNameAndAttr = '%s.%s' % (self.name, locSourceAttrName)

        # Add and set soure attribute for reference later
        cmds.addAttr(self.name, ln=locSourceAttrName, dt='string')
        cmds.setAttr(locNameAndAttr, self.source, lock=True, keyable=False, channelBox=False, typ='string')

    @restoreContextDecorator
    def match(self):

        self.snap(self.source)

    @suspendRefreshDecorator
    @restoreContextDecorator
    def matchAnim(self, atKeys=False):

        self.snapAnim(self.source, atKeys=atKeys)
