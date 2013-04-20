def whPlayblast(camera):
    format = "image"
    sound = soundFileName
    clearCache = True
    viewer = False
    showOrnaments = False
    percent = 100
    quality = 100
    compression = "jpeg"
    widthHeight = blastWidth blastHeight
    start = highlight[0]
    end = highlight[1]
    filename = saveLocation + playBlastFileName
    framePadding = False

    playblast(format=format, framePadding=framePadding, sounds=sound, clearCache=clearCache, viewer=viewer, showOrnaments=showOrnaments, percent=percent, quality=quality, compression=compression, widthHeight=widthHeight, startTime=start, endTime=end, filename=filename)

# Get settings
    # Default Resolution
    # Current Panel
    # Panel Swatchest

# Clean View
# Playblast
# Reset View

# Open file with itview
# VersionUp file


import maya.cmds as cmds

def getActiveModelPanel():
    panel = cmds.getPanel(wf=True)
    if cmds.getPanel(to=panel) == "modelPanel":
        return panel

def getModelPanelOptionsState(panel):
    options = ["nc","ns","pm","sds","pl","lt","ca","j","ikh","df","dy","fl","hs","fo","lc","dim","ha","pv","tx","str","gr","cv","hu"]
    state = []
    for i in len(options):
        state[i] = cmds.modelEditor(panel, q=True, option[i]=True)
    return state

def setModelPanelOptionsState(panel, state):
    options = ["nc","ns","pm","sds","pl","lt","ca","j","ikh","df","dy","fl","hs","fo","lc","dim","ha","pv","tx","str","gr","cv","hu"]
    for i in len(options):
        cmds.modelEditor(panel, e=True, option[i]=state[i])

activePanel = getActiveModelPanel()
if activePanel:
    state = getModelPanelOptionsState(activePanel)