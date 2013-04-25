import maya.cmds as cmds


# Yuck, this is so messy
class manipMode(object):

    '''For toggling orientation of your manipulators'''

    def __init__(self, manip):
        super(manipMode, self).__init__()

        self.tool = str(cmds.currentCtx())

        def printMode(self, mode, changed=False):

            if changed:
                print 'Changed to %s Mode' % mode
            else:
                print 'Currently in %s Mode' % mode

        def rotateModePress():

            cmds.RotateToolMarkingMenu()

            mode = int(cmds.manipRotateContext('Rotate', q=True, mode=True))

            if self.tool == 'RotateSuperContext':
                if mode == 0:
                    cmds.manipRotateContext('Rotate', e=True, mode=2)
                    # 0 = Local, 1 = Global, 2 = Gimbal
                    self.printMode('Gimbal', changed=True)
                elif mode == 2:
                    cmds.manipRotateContext('Rotate', e=True, mode=True)
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

        def rotateModeRelease():
            cmds.RotateToolMarkingMenuPopDown()

        def translateModePress():
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
                    cmds.manipMoveContext('Move', e=True, mode=True)
                    self.printMode('Local', changed=True)

            elif mode == 0:
                self.printMode('Object')
            elif mode == 2:
                self.printMode('World')
            elif mode == 1:
                self.printMode('Local')

        def translateModeRelease():
            cmds.TranslateToolWithSnapMarkingMenuPopDown()

        def scaleModePress():
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
                    cmds.manipScaleContext('Scale', e=True, mode=True)
                    self.printMode('Local', changed=True)

            elif mode == 0:
                self.printMode('Object')
            elif mode == 2:
                self.printMode('World')
            elif mode == 1:
                self.printMode('Local')

        def scaleModeRelease():
            cmds.ScaleToolWithSnapMarkingMenuPopDown()
