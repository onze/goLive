import __builtin__

from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject
from panda3d.core import ConfigVariableDouble,ConfigVariableInt,ConfigVariableString,WindowProperties 

from game_setup import Game_setup
from gaming.gframe import GFrame
from main_menu import Main_menu
from q3 import Console
import widget

class Screen(DirectObject):
	'''
	the screen manipulates Frames (subclasses of) that present stuff to the user.
	'''
	sgn_intro_done='screen.intro_done'
	sgn_main_menu_join='screen.sgn_main_menu_join'
	sgn_main_menu_create='screen.sgn_main_menu_create'
	def __init__(self):
		DirectObject.__init__(self)
		#create main window
		base=ShowBase()
		__builtin__.base=base
		props = WindowProperties()
		props.setFullscreen(True)
		self.width=ConfigVariableInt('win-width').getValue()
		self.height=ConfigVariableInt('win-height').getValue()
		props.setSize(self.width,self.height)
		base.win.requestProperties(props)
		base.disableMouse()
		#set fps limit
		globalClock=ClockObject.getGlobalClock() 
		globalClock.setMode(ClockObject.MLimited) 
		globalClock.setFrameRate(ConfigVariableDouble('clock-frame-rate').getValue())
		__builtin__.screen=self
		__builtin__.gui=pixel2d.attachNewNode('Screen.gui')
		#gui is the node for 2d rendering, scaled to the screen resolution,
		#with origin at bottom-left, and max at top-right
		gui.setZ(gui,-self.height)
		__builtin__.console = Console(print_messenger_events=True)
		__builtin__.out=console.out
		console.request('Open')
		__builtin__.mouse=base.pointerWatcherNodes[0]
		#is used as a stack. stores frames showed to the user (top at the front of the screen)
		self.frames=[]

	def open_game_setup(self):
		self.frame=Game_setup(w=self.width,h=self.height)
		self.frames.append(self.frame)
		self.frame.open()

	def close_game_setup(self):
		self.frame.close()
		self.frame=None
		self.frames.pop(-1)

	def open_gaming(self):
		self.frame=GFrame(w=self.width,h=self.height)
		self.frames.append(self.frame)
		self.frame.open()

	def close_gaming(self):
		pass

	def open_intro(self):
		self.intro_message=OnscreenText(text='intro',style=1,fg=(1,1,1,1),pos=(.87,-.95),scale=.07)
		taskMgr.doMethodLater(ConfigVariableDouble('intro-delay').getValue(),messenger.send,Screen.sgn_intro_done, extraArgs = [Screen.sgn_intro_done])

	def close_intro(self):
		self.intro_message.destroy()
		del self.intro_message

	def open_main_menu(self):
		self.frame=Main_menu(w=self.width,h=self.height)
		self.frames.append(self.frame)
		self.frame.open()

	def close_main_menu(self):
		self.frame.close()
		self.frame=None
		self.frames.pop(-1)
