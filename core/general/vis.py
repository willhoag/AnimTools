import maya.cmds as cmds
import maya.mel as mel


# Ideal
# ModelVis('nurbsCurves').toggle()
# ModelVis('nurbsCurves').on()
# ModelVis('nurbsCurves').off()

# Pretty damn messy!!!
class ModelVis(object):

    """docstring for toggleViz"""

    def __init__(self):
        super(ModelVis, self).__init__()
        self.panel = str(cmds.getPanel())

    def toggle(self, onOff):

        if onOff:
            onOff = 0
        else:
            onOff = 1

        return onOff

    def nurbsCurves(self):
        viz = int(cmds.modelEditor(self.panel, query=True, nurbsCurves=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, edit=True, nurbsCurves=onOff)

    def locators(self):
        viz = int(cmds.modelEditor(self.panel, query=True, locators=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, edit=True, locators=onOff)

    def polygons(self):
        viz = int(cmds.modelEditor(self.panel, query=True, polymeshes=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, edit=True, polymeshes=onOff)

    def nurbsSurfaces(self):
        viz = int(cmds.modelEditor(self.panel, query=True, nurbsSurfaces=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, edit=True, nurbsSurfaces=onOff)

    def joints(self):
        viz = int(cmds.modelEditor(self.panel, query=True, joints=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, joints=True, edit=onOff)

    def isolateSelect(self):
        panelType = str(cmds.getPanel(to=self.panel))
        if panelType is 'modelPanel':
            state = int(cmds.isolateSelect(self.panel, query=True, statedit=True))
            if state:
                mel.enableIsolateSelect(self.panel, False)
            else:
                mel.enableIsolateSelect(self.panel, True)

    def wireframeOnShaded(self):
        viz = int(cmds.modelEditor(self.panel, query=True, wireframeOnShaded=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, wireframeOnShaded=True, edit=onOff)

    def deformers(self):
        viz = int(cmds.modelEditor(self.panel, query=True, deformers=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, deformers=True, edit=onOff)

    def xRay(self):
        viz = int(cmds.modelEditor(self.panel, query=True, xray=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, xray=True, edit=onOff)

    def xRayJoints(self):
        viz = int(cmds.modelEditor(self.panel, query=True, jointXray=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, jointXray=True, edit=onOff)

    def grid(self):
        viz = int(cmds.modelEditor(self.panel, query=True, grid=True))
        onOff = self.toggle(viz)
        cmds.modelEditor(self.panel, grid=True, edit=onOff)
