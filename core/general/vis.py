# script created by pymel.tools.mel2py from mel file:
# /Users/willhoag/Library/Preferences/Autodesk/maya/scripts/my_scripts/toggleVis.mel

import maya.cmds as cmds
import maya.mel as mel


class ToggleVis(object):
    """docstring for toggleViz"""
    def __init__(self):
        super(ToggleVis, self).__init__()
        self.panel = str(cmds.getPanel())

    def nurbsCurves(self):
        viz = int(cmds.modelEditor(self.panel, q=1, nurbsCurves=1))

        if viz == 1:
            cmds.modelEditor(self.panel, e=1, nurbsCurves=0)
        else:

            cmds.modelEditor(self.panel, e=1, nurbsCurves=1)

    def locators(self):
        viz = int(cmds.modelEditor(self.panel, q=1, locators=1))
        if viz == 1:
            cmds.modelEditor(self.panel, locators=0, e=1)
        else:

            cmds.modelEditor(self.panel, locators=1, e=1)

    def polygons(self):
        viz = int(cmds.modelEditor(self.panel, q=1, polymeshes=1))
        if viz == 1:
            cmds.modelEditor(self.panel, e=1, polymeshes=0)
        else:

            cmds.modelEditor(self.panel, e=1, polymeshes=1)

    def nurbsSurfaces(self):
        viz = int(cmds.modelEditor(self.panel, q=1, nurbsSurfaces=1))
        if viz == 1:
            cmds.modelEditor(self.panel, e=1, nurbsSurfaces=0)
        else:

            cmds.modelEditor(self.panel, e=1, nurbsSurfaces=1)

    def joints(self):
        viz = int(cmds.modelEditor(self.panel, q=1, joints=1))
        if viz == 1:
            cmds.modelEditor(self.panel, joints=0, e=1)
        else:

            cmds.modelEditor(self.panel, joints=1, e=1)

    def isolateSelect(self):
        panelType = str(cmds.getPanel(to=self.panel))
        if panelType is 'modelPanel':
            state = int(cmds.isolateSelect(self.panel, q=1, state=1))
            if state:
                mel.enableIsolateSelect(self.panel, False)
            else:
                mel.enableIsolateSelect(self.panel, True)

    def wireframeOnShaded(self):
        viz = int(cmds.modelEditor(self.panel, q=1, wireframeOnShaded=1))
        if viz == 1:
            cmds.modelEditor(self.panel, wireframeOnShaded=0, e=1)
        else:

            cmds.modelEditor(self.panel, wireframeOnShaded=1, e=1)

    def deformers(self):
        viz = int(cmds.modelEditor(self.panel, q=1, deformers=1))
        if viz == 1:
            cmds.modelEditor(self.panel, deformers=0, e=1)
        else:

            cmds.modelEditor(self.panel, deformers=1, e=1)

    def xRay(self):
        viz = int(cmds.modelEditor(self.panel, q=1, xray=1))
        if viz == 1:
            cmds.modelEditor(self.panel, xray=0, e=1)
        else:

            cmds.modelEditor(self.panel, xray=1, e=1)

    def xRayJoints(self):
        viz = int(cmds.modelEditor(self.panel, q=1, jointXray=1))
        if viz == 1:
            cmds.modelEditor(self.panel, jointXray=0, e=1)
        else:

            cmds.modelEditor(self.panel, jointXray=1, e=1)

    def grid(self):
        viz = int(cmds.modelEditor(self.panel, q=1, grid=1))
        if viz == 1:
            cmds.modelEditor(self.panel, grid=0, e=1)
        else:

            cmds.modelEditor(self.panel, grid=1, e=1)
