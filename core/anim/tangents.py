import maya.cmds as cmds
from itertools import cycle
from wh.core.util.strings import userMessage


class DefaultTangents:
    '''A class for managing the default tangent types'''

    def __init__(self):
        self.current = dict()
        self.update()

    def set(self, itt="auto", ott="auto"):
        '''For setting the default tangent types'''
        cmds.keyTangent(g=True, itt=itt, ott=ott)
        self.update()

    def update(self):
        '''To update the classes attributes to match the current default tangent types'''
        current = cmds.keyTangent(q=True, g=True)[0:2]
        self.current['itt'] = current[0]
        self.current['ott'] = current[1]

    def toggle(self, *toggles):
        '''
        Takes an arbitrary amount of tupples for in tangent and out tangent and cycles through them.
        Example Usage: DefaultTangents().toggle(('auto', 'auto'), ('clamped', 'step'))
        - This toggles between auto tangents and stepped tangents  
        '''
        self.update()

        # set default
        tangents = toggles[0]

        # need in order to get next value in loop
        cycleToggles = cycle(toggles)

        # prime the pump
        next = cycleToggles.next()
        # reset tangents to next one if it's at one already
        for toggle in toggles:

            next = cycleToggles.next()

            # if out tangents are equlal
            if self.current['ott'] == toggle[1]:

                tangents = next

        # set default tangents type
        self.set(itt=tangents[0], ott=tangents[1])

        userMessage("Default tangents set to " + str(tangents))

        # update class
        self.update()
