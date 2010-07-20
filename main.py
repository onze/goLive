
import __builtin__
import sys
#load default config
import default
default.load_panda_default()
from pandac.PandaModules import loadPrcFile
loadPrcFile(sys.path[0]+'/Config.prc')

from panda3d.core import ConfigVariableBool,ConfigVariableString,PStatClient
from direct.fsm import FSM
from direct.showbase.MessengerGlobal import messenger
from direct.task.TaskManagerGlobal import taskMgr

from screen.screen import Screen
from screen.gaming.gentity import GEntity
from server.serverproxy import ServerProxy
from server import network
if ConfigVariableBool('dev-mode').getValue():
	from tools import pstat

class GameClient(FSM.FSM):
	def __init__(self):
		FSM.FSM.__init__(self, 'GameClient.fsm')
		self.defaultTransitions = {
			'Game_setup':['Main_menu', 'Gaming'],
			'Gaming':['Stats', 'Pause', 'Quit'],
			'Init':['Intro'],
			'Intro':['Main_menu'],
			'Main_menu':['Options', 'Game_setup', 'Quit', 'Load_game'],
			'Options':['Main_menu', 'Gaming'],
			'Pause':['Main_menu', 'Quit', 'Options', 'Gaming'],
			'Quit':[],
			'Stats':['Game_setup'],
			}
		#any method in this global list gets called once a frame
		__builtin__.update_list=[]
		#any object in this global list gets its dispose method called by current frame's end
		__builtin__.dispose_list=[]
		self.is_running=True
		self.screen=None
		self.fake_keypresses=['q','a']#,'mouse1','mouse1-up','space']

	def enterGame_setup(self):
		self.screen.open_game_setup()
		self.acceptOnce(self.screen.frame.sgn_start, self.demand, extraArgs=['Gaming'])
		if ConfigVariableBool('dev-mode').getValue():
			messenger.send(self.screen.frame.sgn_start)

	def exitGame_setup(self):
		#TODO grab setup options here
		self.game_conf=self.screen.frame.config
		self.screen.close_game_setup()

	def enterGaming(self):
		self.proxy=ServerProxy()
		self.proxy.send_config(self.game_conf)
		self.screen.open_gaming()
		del self.game_conf
		update_list.append(self.update_gaming)
		#meant for synchro with server.
		#not intensely used until now, but would when server is ran in its own thread,
		#or when it is separated for real networked gaming.
		self.frame_no=GEntity.frame_no=0

	def exitGaming(self):
		self.screen.close_gaming()
		update_list.remove(self.update_gaming)

	def enterInit(self):
		'''
		init of main/global structures
		'''
		self.screen = Screen()
		if ConfigVariableBool('dev-mode').getValue():
			self.update_gaming=pstat(self.update_gaming)			
			PStatClient.connect()
		taskMgr.add(self.update, 'GameClient.update')
		self.acceptOnce('escape',self.demand,extraArgs=['Quit'])
		self.demand('Intro')

	def exitInit(self):pass

	def enterIntro(self):
		'''
		game introduction. video/screens.
		'''
		#skip to main menu with enter
		self.acceptOnce(ConfigVariableString('key-confirm').getValue(), self.demand,extraArgs=['Main_menu'])
		#go to main menu when screen is done
		self.acceptOnce(Screen.sgn_intro_done, self.demand,extraArgs=['Main_menu'])
		#show splash intro
		self.screen.open_intro()
		if ConfigVariableBool('dev-mode').getValue():
			self.demand('Main_menu')

	def exitIntro(self):
		self.screen.close_intro()
		self.ignore(ConfigVariableString('key-confirm').getValue())
		self.ignore(Screen.sgn_intro_done)

	def enterMain_menu(self):
		'''
		menu offers 4 choices:
		-play game
		-load game
		-options
		-quit
		'''
		self.screen.open_main_menu()
		self.acceptOnce(self.screen.frame.sgn_play, self.demand,extraArgs=['Game_setup'])
		if ConfigVariableBool('dev-mode').getValue():
			self.demand('Game_setup')

	def exitMain_menu(self):
		self.screen.close_main_menu()

	def enterOptions(self):pass
	def exitOptions(self):pass
	def enterPause(self):pass
	def exitPause(self):pass

	def enterQuit(self):
		'''
		last cleanup before closing the window.
		'''
		#TODO clean close
		self.screen.destroy()
		del self.screen
		self.is_running = False

	def exitQuit(self):pass

	def update_gaming(self):
#		out('client update',frame_no=self.frame_no)
		void=True		
		self.frame_no+=1
		GEntity.frame_no=self.frame_no
		#process data from server (server's update included)
		for d in self.proxy.new_data:
			void=False
			#TODO: process frame info
			#some of them are to be processed here
			if network.stc_start_game in d:
				out('network.stc_start_game')
				self.screen.frame.start_game()
			elif network.stc_end_game in d:
				out('network.stc_end_game')
				self.demand('Stats')
			#if etc
			#the rest is given to the gframe, responsible for the graphic stuff
			else:
				self.screen.frame.process_server_input(d)
		if void:
			if len(self.fake_keypresses):
				messenger.send(self.fake_keypresses[0])
				self.fake_keypresses.pop(0)
		for o in __builtin__.dispose_list:o.dispose()
		__builtin__.dispose_list=[]

	def update(self, task):
		'''
		main update method. runs the whole time.
		other updates can register to update_list to get called every frame.
		'''
		[f() for f in update_list]
		return task.again

gc = GameClient()
gc.request('Init')

while gc.is_running:
	taskMgr.step()

'''
#better loop logic
#fps=ConfigVariableDouble('fps')
#skip_frames=ConfigVariableDouble('skip_frames')
#max_frames_skip=ConfigVariableDouble('max_frames_skip')
#next_display=time.clock()
#while running:
#loops=0
#while time.clock()>next_display and loops<max_frames_skip:
#update game
#taskMgr.step()
#next_display+=skip_frames
#loops+=1

#interpolation=(time.clock()+skip_frames-next_game_tick)/skip_frames
#display_game(interpolation)
#udpate screen
'''

