Anim Tools
==========
A Maya Python Framework for developing ideal workflows

# Description
This is a python package that is meant become a comprehensive set of workflow tools. It likely has a large animation bias as that is my core use of it, but much of what's in here could be used in other maya related departments ( ex: modeling, rigging, layout, etc. ).

# About
Setting up custom workflows in the past meant going to creativecrash (or previously highend3d) for scripts, bumming some off your friends, or writing your own scripts. We've all been looking for these scripts like scavenging for collectors items in a garage sale block party! Let's not even go into trying to keep your scripts updated...

It's starting to get better though. Some awesome people are developing studio quality tools that hopefully will ease the pain. Check out Red9 if you are looking at having a studio-quality pipeline. CG Monks have a bunch of great animation stuff too. Also, there are some tools that are for sale which can be quite good as well. Probably a lot more I'm forgetting to mention.

I'm starting to see some Maya projects pop up here and there on github. It would be great if we could contribute to each others projects. Feel free to fork this repo and show me why I'm not very good at python programming yet. :p


# Documentation

Note! This is currently very WIP. Most of it's functioning, but I wouldn't be surprised if it has bugs. Also, there is almost no inline documentation, and there are some coding inconsistencies as well like sometimes using a dict and sometimes using a list for similar items. <-- Annoying! Will work to clean those up and write some code docs. Check out the issues and write some if you see any.


## Usage:

Some of the modules are useful out of the box like making quick hotkeys:

'''
from wh.core.general.hotkey import hotkey

# Easy Hotkeys!
hotkey('A', alt=True).setupHotkey('AttributeEditor')
hotkey('C', alt=True).setupHotkey('ConnectionEditor')
hotkey('G', alt=True).setupHotkey('GraphEditor')

# Custom ones too
hotkey('D', ctl=True).setup('wh.ModelVis().deformers()')
hotkey('G', ctl=True).setup('wh.ModelVis().grid()')
hotkey('I', ctl=True).setup('wh.ModelVis().isolateSelect()')
'''

Other useful commands

'''
# Skipping undo and playing that frame of audio
CurrentTime.nextKey()
CurrentTime.prevKey()
CurrentTime.nextFrame()
CurrentTime.prevFrame()

# Sets the range slider to highlighted timeline
Range().set() # Sets range at highlighted time
Range().set(range=['start': 20, 'end': 62]) # Sets range at specified time
Range().setIn() # Sets in range at current time
Range().setOut() # Sets out range at current time

SnapObject('pSphere1').snap('pCube1') # snap pSphere1 to pCube1
SnapObject('pSphere1').snapAnim('pCube1') # snap animation from pSphere1 to pCube1
SnapObject('pSphere1').snapAnim('pCube1', atKeys=True) # snap animation from pSphere1 to pCube1 just at keys
MatchLocator('pSphere1').match() # make locator and match to pSphere1
MatchLocator('pSphere1').matchAnim() # make locator and match anim to pSphere1
MatchLocator('pSphere1').matchAnim(atKeys=True) # make locator and match keys of pSphere1

KeyFrames().breakdown(30) # breakdown 30%
KeyFrames().initialize() # set to zero
KeyFrames().bake() # bake selected frames
KeyFrames().merge() # merge selected keyframes
KeyFrames(step=2).rekey() # rekey on 2's or 4's

makeShelfButton('Command()' sourceType='python')
'''

Generally, I've found the most useful commands operate based on user defined parameters. These can be things like selected objects, selected channels, highlighted timeline, selected curves and selected keys. I call these action items have made them into reusable and flexible classes to make developing with these inputs quick and easy.

core.util.action
'''
# With user input
for frame in ActionFrames() # operate over a highlighted framerange
    for node in ActionNodes() # operate over selected nodes
        for attr in ActionAttrs(node) # operate over selected channels

for key in ActionKeyFrames() # operate over keyframes of selected nodes within a selected framerange
	for curve in ActionCurves() # operate over selected curves
		for key in ActionKeys(curve) # operate over selected keys

# Custom input

for frame in ActionFrames(frameRange=[20, 35] step=2) # operate over specified framerange every other frame
    for node in ActionNodes(nodes = objectList) # operate over specified nodes
        for attr in ActionAttrs(node, attrs=[rx, ry, tz]) # operate over specified channels

for key in ActionKeyFrames(nodes=objectList, frameRange=[10, 42]) # operate over keyframes of specified nodes within a specified framerange
	for curve in ActionCurves(curves=[rz, ty, tz, tx]) # operate over specified curves
		for key in ActionKeys(curve, keys=[1, 3, 42]) # operate over specified keys
'''

## Other things you can do are:

toggle visibility of things like wireframe on shaded, isolated objects, polygons, nurbsSurfaces, curves etc.

rig independent selection sets: make a set for the finger controls and then select fingers for any character on the fly based on controls you already have selected.

cycle through manipulator orientation using 'w', 'e' & 'r'