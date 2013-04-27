import maya.cmds as cmds
import maya.mel as mel


# Ideal
# ModelVis('nurbsCurves').toggle()
# ModelVis('nurbsCurves').on()
# ModelVis('nurbsCurves').off()

# Right now
# ModelVis().nurbsCurves()

# Pretty damn messy!!!
class ModelVis(object):

    """ModelVis().locators()"""

    def __init__(self):
        super(ModelVis, self).__init__()
        self.panel = str(cmds.getPanel(withFocus=True))

    def nurbsCurves(self):
        viz = cmds.modelEditor(self.panel, query=True, nurbsCurves=True)
        cmds.modelEditor(self.panel, edit=True, nurbsCurves=not viz)

    def locators(self):
        viz = cmds.modelEditor(self.panel, query=True, locators=True)
        cmds.modelEditor(self.panel, edit=True, locators=not viz)

    def polygons(self):
        viz = cmds.modelEditor(self.panel, query=True, polymeshes=True)
        cmds.modelEditor(self.panel, edit=True, polymeshes=not viz)

    def nurbsSurfaces(self):
        viz = cmds.modelEditor(self.panel, query=True, nurbsSurfaces=True)
        cmds.modelEditor(self.panel, edit=True, nurbsSurfaces=not viz)

    def joints(self):
        viz = cmds.modelEditor(self.panel, query=True, joints=True)
        cmds.modelEditor(self.panel, joints=True, edit=not viz)

    def isolateSelect(self):
        panelType = str(cmds.getPanel(to=self.panel))
        if panelType is 'modelPanel':
            state = cmds.isolateSelect(self.panel, query=True, statedit=True)
            mel.enableIsolateSelect(self.panel, not state)

    def wireframeOnShaded(self):
        viz = cmds.modelEditor(self.panel, query=True, wireframeOnShaded=True)
        cmds.modelEditor(self.panel, wireframeOnShaded=True, edit=not viz)

    def deformers(self):
        viz = cmds.modelEditor(self.panel, query=True, deformers=True)
        cmds.modelEditor(self.panel, deformers=True, edit=not viz)

    def xRay(self):
        viz = cmds.modelEditor(self.panel, query=True, xray=True)
        cmds.modelEditor(self.panel, xray=True, edit=not viz)

    def xRayJoints(self):
        viz = cmds.modelEditor(self.panel, query=True, jointXray=True)
        cmds.modelEditor(self.panel, jointXray=True, edit=not viz)

    def grid(self):
        viz = cmds.modelEditor(self.panel, query=True, grid=True)
        cmds.modelEditor(self.panel, grid=True, edit=not viz)
