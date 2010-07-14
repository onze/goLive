#import __builtin__

from direct.gui.DirectGui import *
__package__='screen.game_setup'
from server import default
from screen.widgetwrapper import Button,Frame,Spacer
from screen import layout

class Game_setup(Frame):
	sgn_start='Game_setup.sgn_start'

	def __init__(self,*args,**kwargs):
		kwargs['layout']=layout.HLayout
		Frame.__init__(self,*args,**kwargs)
		res=loader.loadModel('data/gui/game_setup.egg')
		self.resources = {	'start_btn':res.find('**/game_setup.start_btn')}
		#default config =P
		self.config=dict(default.game_conf)

	def open(self):
		[Spacer(parent=self) for i in range(2)]
		self.right_frame=Frame( layout=layout.VLayout,
								parent=self,
								pref_w=180)
		Spacer(parent=self.right_frame)
		self.start_btn=Button(	pref_h=70,
								p3dobject=DirectButton(geom=(self.resources['start_btn']),
														borderWidth=(0,0),
														command=messenger.send, extraArgs=[Game_setup.sgn_start]),
								parent=self.right_frame)
		[Spacer(parent=self.right_frame) for i in range(5)]
		Spacer(parent=self)

		self.message=OnscreenText(text='game setup',style=1,fg=(1,1,1,1),pos=(.87,-.95),scale=.07)

	def close(self):
		del self.right_frame
		self.start_btn.p3dobject.destroy()
		del self.start_btn
		self.message.destroy()
		del self.message

