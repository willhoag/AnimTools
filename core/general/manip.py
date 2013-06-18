import maya.cmds as cmds


# Yuck, this is so messy
class ManipMode(object):

    '''For toggling orientation of your manipulators'''

    def __init__(self):
        super(ManipMode, self).__init__()

        self.tool = str(cmds.currentCtx())

    @staticmethod
    def printMode(mode, changed=False):

        if changed:
            print 'Changed to %s Mode' % mode
        else:
            print 'Currently in %s Mode' % mode

    def rotateModePress(self):

        # modes = {'Gimbal': 2, 'Global': 1, 'Local': 0}

        cmds.RotateToolMarkingMenu()

        mode = int(cmds.manipRotateContext('Rotate', q=True, mode=True))

        if self.tool == 'RotateSuperContext':
            if mode == 0:
                cmds.manipRotateContext('Rotate', e=True, mode=2)
                # 0 = Local, 1 = Global, 2 = Gimbal
                self.printMode('Gimbal', changed=True)
            elif mode == 2:
                cmds.manipRotateContext('Rotate', e=True, mode=1)
                self.printMode('Global', changed=True)
            elif mode == 1:
                cmds.manipRotateContext('Rotate', e=True, mode=0)
                self.printMode('Local', changed=True)

        elif mode == 0:
            self.printMode('Local')
        elif mode == 2:
            self.printMode('Gimbal')
        elif mode == 1:
            self.printMode('Global')

    @staticmethod
    def rotateModeRelease():
        cmds.RotateToolMarkingMenuPopDown()

    def translateModePress(self):
        cmds.TranslateToolWithSnapMarkingMenu()

        mode = int(cmds.manipMoveContext('Move', q=True, mode=True))

        if self.tool == 'moveSuperContext':
            if mode == 1:
                # 0 = Object, 1 = Local, 2 = World, 3 = Normal, 4 = Rotation Axis
                cmds.manipMoveContext('Move', e=True, mode=2)
                self.printMode('World', changed=True)
            elif mode == 2:
                cmds.manipMoveContext('Move', e=True, mode=0)
                self.printMode('Object', changed=True)
            elif mode == 0:
                cmds.manipMoveContext('Move', e=True, mode=1)
                self.printMode('Local', changed=True)

        elif mode == 0:
            self.printMode('Object')
        elif mode == 2:
            self.printMode('World')
        elif mode == 1:
            self.printMode('Local')

    @staticmethod
    def translateModeRelease():
        cmds.TranslateToolWithSnapMarkingMenuPopDown()

    def scaleModePress(self):
        cmds.ScaleToolWithSnapMarkingMenu()

        mode = int(cmds.manipScaleContext('Scale', q=True, mode=True))
        if self.tool == 'scaleSuperContext':
            if mode == 1:
                # 0 = Object, 1 = Local, 2 = World
                cmds.manipScaleContext('Scale', e=True, mode=2)
                self.printMode('World', changed=True)
            elif mode == 2:
                cmds.manipScaleContext('Scale', e=True, mode=0)
                self.printMode('Object', changed=True)
            elif mode == 0:
                cmds.manipScaleContext('Scale', e=True, mode=1)
                self.printMode('Local', changed=True)

        elif mode == 0:
            self.printMode('Object')
        elif mode == 2:
            self.printMode('World')
        elif mode == 1:
            self.printMode('Local')

    @staticmethod
    def scaleModeRelease():
        cmds.ScaleToolWithSnapMarkingMenuPopDown()
