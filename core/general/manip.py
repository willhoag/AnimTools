# script created by pymel.tools.mel2py from mel file:
# /Users/willhoag/Library/Preferences/Autodesk/maya/scripts/my_scripts/toggleRotateMode.mel

from pymel.all import *

def toggleRotateModePress():
	currentTool=str(currentCtx())
	RotateToolMarkingMenu()
	rotX=int(manipRotateContext('Rotate',q=1,mode=1))
	if currentTool == "RotateSuperContext":
		if rotX == 0:
			manipRotateContext('Rotate',e=1,mode=2)
			# 0 = Local, 1 = Global, 2 = Gimbal
			print "\n Changed to Gimbal Mode \n"
			
		
		elif rotX == 2:
			manipRotateContext('Rotate',e=1,mode=1)
			print "\n Changed to Global Mode \n"
			
		
		elif rotX == 1:
			manipRotateContext('Rotate',e=1,mode=0)
			print "\n Changed to Local Mode \n"
			
		
	
	elif rotX == 0:
		print "\n Currently in Local Mode \n"
		
	
	elif rotX == 2:
		print "\n Currently in Gimbal Mode \n"
		
	
	elif rotX == 1:
		print "\n Currently in Global Mode \n"
		
	

def toggleRotateModeRelease():
	RotateToolMarkingMenuPopDown()
	

def toggleTranslateModePress():
	currentTool=str(currentCtx())
	TranslateToolWithSnapMarkingMenu()
	transX=int(manipMoveContext('Move',q=1,mode=1))
	if currentTool == "moveSuperContext":
		if transX == 1:
			manipMoveContext('Move',e=1,mode=2)
			# 0 = Object, 1 = Local, 2 = World, 3 = Normal, 4 = Rotation Axis
			print "\n Changed to World Mode \n"
			
		
		elif transX == 2:
			manipMoveContext('Move',e=1,mode=0)
			print "\n Changed to Object Mode \n"
			
		
		elif transX == 0:
			manipMoveContext('Move',e=1,mode=1)
			print "\n Changed to Local Mode \n"
			
		
	
	elif transX == 0:
		print "\n Currently in Object Mode \n"
		
	
	elif transX == 2:
		print "\n Currently in World Mode \n"
		
	
	elif transX == 1:
		print "\n Currently in Local Mode \n"
		
	

def toggleTranslateModeRelease():
	TranslateToolWithSnapMarkingMenuPopDown()
	

def toggleScaleModePress():
	currentTool=str(currentCtx())
	ScaleToolWithSnapMarkingMenu()
	scaleX=int(manipScaleContext('Scale',q=1,mode=1))
	if currentTool == "scaleSuperContext":
		if scaleX == 1:
			manipScaleContext('Scale',e=1,mode=2)
			# 0 = Object, 1 = Local, 2 = World
			print "\n Changed to World Mode \n"
			
		
		elif scaleX == 2:
			manipScaleContext('Scale',e=1,mode=0)
			print "\n Changed to Object Mode \n"
			
		
		elif scaleX == 0:
			manipScaleContext('Scale',e=1,mode=1)
			print "\n Changed to Local Mode \n"
			
		
	
	elif scaleX == 0:
		print "\n Currently in Object Mode \n"
		
	
	elif scaleX == 2:
		print "\n Currently in World Mode \n"
		
	
	elif scaleX  ==1:
		print "\n Currently in Local Mode \n"
		
	

def toggleScaleModeRelease():
	ScaleToolWithSnapMarkingMenuPopDown()
	

