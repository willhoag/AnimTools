import maya.cmds as cmds
from wh.util.strings import addPrefix, getPrefix

def selectWithPrefixs(names, add=False):
    selection = cmds.ls(sl=True)
    prefixes = set()
    select = []

    for s in selection:
        prefixes.add(getPrefix(s, '_'))
    
    for prefix in prefixes:
        for name in names:
            select.append(addPrefix(prefix, '_', name))

    cmds.select(select, add=add)