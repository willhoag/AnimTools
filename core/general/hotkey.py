import maya.cmds as cmds
import re

class hotkey:

	'''import pymel.core as cmds

	Basic Usage
	x = hotkey('g').setup('whSetZero')

	Set Modifiers
	x = hotkey('g', alt=True, ctl=True, cmd=True).setup('whSetZero', name='SetZeroCommand', sourceType='mel', annotation='This is a command to set selected channels to their default values')

	Other Useful Functions
	cmds.runtime.SavePreferences()
	cmds.hotkey(factorySettings=True)'''

	name = None
	command = None
	commandName = None
	sourceType = None
	annotation = None

	def __init__(self, key, alt=False, ctl=False, cmd=False, shift=False, release=False):

		if not shift:
			if key.isupper():
				shift = True

		if shift:
			key = key.upper()

		self.alt = alt
		self.ctl = ctl
		self.cmd = cmd
		self.shift = shift
		self.release = release
		self.key = key

	def setup(self, command, name=None, sourceType='python', annotation=''):
		"""Sets up hotkey linking the hotkey instance to the command."""
		
		if not name: # Default using first part of command if name is not explicitly given
			name = re.sub(r'\W+', '', command.split()[0])  # remove non alphanumeric characters from command for name

		self.name = name
		self.command = command
		self.sourceType = sourceType
		self.annotation = annotation

		# Build
		self.setupHotkey(name, sourceType=sourceType)
		self.setupCommand(command, name, sourceType, annotation)

	def setupHotkey(self, name, sourceType='mel'):
		"""Sets up the hotkey and nameCommand only. This is useful when linking to a maya runtimeCommand."""
		
		self.name = name
		self.commandName = name + 'NameCommand' # Make names consistant with Maya's convention 
		self.sourceType=sourceType

		if self.release:
			cmds.hotkey(k=self.key, alt=self.alt, ctl=self.ctl, cmd=self.cmd, rn=self.commandName)
		else:
			cmds.hotkey(k=self.key, alt=self.alt, ctl=self.ctl, cmd=self.cmd, n=self.commandName)

		cmds.nameCommand(self.commandName, ann=self.commandName, c=self.name, stp=self.sourceType)

	def setupCommand(self, command, name, sourceType, annotation):
		"""Makes the nameCommand and the runtimeCommand that is linked to by the hotkey"""

		cmds.runTimeCommand(self.name, ann=self.annotation, cat='User', c=self.command, cl=self.sourceType)
