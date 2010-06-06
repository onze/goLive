
from direct.fsm import FSM
from direct.gui.DirectGui import DirectButton
from direct.showbase.DirectObject import DirectObject
from panda3d.core import KeyboardButton

from ..widgetwrapper import WidgetWrapper,Frame,Button,Spacer
from ..layout import HLayout
from ..server import network

class Panel(Frame):
	def __init__(self,gmenu):
		Frame.__init__(self,layout=HLayout,parent=gmenu)		
		self.gmenu=gmenu

class UnitSelectionPanel(Panel):
	'''presents the buttons for selection of unit to launch'''
	def __init__(self,gmenu):
		Panel.__init__(self,gmenu)
		#self.add_btn('h_sprinter')
		#self.allow_btn('h_sprinter')
		self.h_sprinter_btn=Button(	pref_w=gmenu.h,
								    pref_h=gmenu.h,
									p3dobject=DirectButton(geom=(gmenu.resources['h_sprinter']),
															borderWidth=(0,0),
															command=gmenu.show_unit_conf,
															extraArgs=['H_sprinter']),
									parent=self) 
		self.v_sprinter_btn=Button(	pref_w=gmenu.h,
									pref_h=gmenu.h,
									p3dobject=DirectButton(geom=(gmenu.resources['v_sprinter']),
															borderWidth=(0,0),
															command=gmenu.show_unit_conf,
															extraArgs=['V_sprinter']),
								parent=self)
		gmenu.accept('q',gmenu.show_unit_conf,extraArgs=['H_sprinter'])
		gmenu.accept('w',gmenu.show_unit_conf,extraArgs=['V_sprinter'])
		
	def close(self):
		self.ignoreAll()
		self.h_sprinter_btn.p3dobject.destroy()
		self.remove_child(self.h_sprinter_btn)
		del self.h_sprinter_btn
		self.v_sprinter_btn.p3dobject.destroy()
		self.remove_child(self.v_sprinter_btn)
		del self.v_sprinter_btn

class UnitConfigurationPanel(Panel,FSM.FSM):
	'''FSM presenting configuration tools for the selected unit to launch.'''
	def __init__(self,gmenu):
		Panel.__init__(self, gmenu)
		FSM.FSM.__init__(self,'GMenu.ConfPanel')
		self._conf={}
	
	def enterBlank(self):
		'''
		blank state: nothing is showed.
		'''
		self._conf={}

	def exitBlank(self):pass	
	
	def enterClose(self):
		del self._conf
		self.ignoreAll()
		
	def exitClose(self):pass

	def enterH_sprinter(self):
		'''
		will display hsprinter conf buttons
		'''
		out('enter hsprinter')
		self.arrow=Button(	pref_w=self.gmenu.h,
						    pref_h=self.gmenu.h,
							p3dobject=DirectButton(geom=(self.gmenu.resources['h_arrow']),
													borderWidth=(0,0),
													command=screen.frame.gmap.enable_tile_selection,
													extraArgs=['single']),
							parent=self)
		self.accept('a',screen.frame.gmap.enable_tile_selection, extraArgs=['single'])
		self._conf['unit_type']='h_sprinter'
	
	def exitH_sprinter(self):
		out('exit hsprinter')
		if screen.frame.gmap.is_tile_selection_enabled:
			screen.frame.gmap.disable_tile_selection()
		self.remove_child(self.arrow)
		self.arrow.p3dobject.destroy()
		del self.arrow
		self._conf['unit_type']=None
	
	def enterV_sprinter(self):
		'''
		will display vsprinter conf buttons
		'''
		out('enter vsprinter')
		self.arrow=Button(	pref_w=self.gmenu.h,
						    pref_h=self.gmenu.h,
							p3dobject=DirectButton(geom=(self.gmenu.resources['v_arrow']),
													borderWidth=(0,0),
													command=screen.frame.gmap.enable_tile_selection,
													extraArgs=['single']),
							parent=self)
		self.accept('a',screen.frame.gmap.enable_tile_selection, extraArgs=['single'])
		self._conf['unit_type']='v_sprinter'
	
	def exitV_sprinter(self):
		out('exit vsprinter')
		if screen.frame.gmap.is_tile_selection_enabled:
			screen.frame.gmap.disable_tile_selection()
		self.remove_child(self.arrow)
		self.arrow.p3dobject.destroy()
		del self.arrow
		self._conf['unit_type']=None
		
	@property
	def conf(self):
		'''
		setup a nice li'll dict contgaining the configuration to pass to the server.
		'''
		self._conf['complete']=True
		if not 'unit_type' in self._conf:
			self._conf['complete']=False
		if screen.frame.gmap.is_tile_selection_enabled:
			tiles=screen.frame.gmap.selected_tiles
			if len(tiles)>0:
				if self._conf['unit_type']=='v_sprinter' or self._conf['unit_type']=='h_sprinter':
					self._conf['x']=tiles[0].x
					self._conf['y']=tiles[0].y
			else:
				self._conf['complete']=False
		else:
			self._conf['complete']=False
		return self._conf

class GMenu(Frame,DirectObject):
	def __init__(self,*args,**kwargs):
		DirectObject.__init__(self)
		kwargs['fill']=165,255,121
		kwargs['fill']=HLayout
		Frame.__init__(self,*args,**kwargs)
		#graphical aspect: [unit_selection_panel | unit_configuration_panel | launch_btn]
		self.sel_pan=UnitSelectionPanel(self)
		self.conf_pan=UnitConfigurationPanel(self)
		self.conf_pan.request('Blank')
		Spacer(parent=self)
		self.launch_btn=Button(	pref_w=self.h*2,
							    pref_h=self.h,
								p3dobject=DirectButton(geom=(self.resources['launch_btn']),
														borderWidth=(0,0),
														command=self.launch_unit),
								parent=self)
		self.accept('enter',self.launch_unit)
		self.accept('space',self.launch_unit)
		self.accept('mouse3',self.launch_unit)
	
	@staticmethod
	def load_resources():
		#load resources
		unit_btn_res=loader.loadModel('data/gui/gmenu/units_btn.egg')
		launch_btn_res=loader.loadModel('data/gui/gmenu/launch_btn.egg')
		unit_conf_res=loader.loadModel('data/gui/gmenu/arrows.egg')
		GMenu.resources = {	'h_sprinter':unit_btn_res.find('**/horizontal_sprinter'),
							'v_sprinter':unit_btn_res.find('**/vertical_sprinter'),
							'launch_btn':launch_btn_res.find('**/launch_btn'),
							'h_arrow':unit_conf_res.find('**/h_arrow'),
							'v_arrow':unit_conf_res.find('**/v_arrow'),
							}

	def close(self):
		self.conf_pan.demand('Close')
		self.sel_pan.close()

	def launch_unit(self):
		'''
		gather conf options to send to the server.
		'''
		conf=self.conf_pan.conf
		out('launching unit',conf=conf)
		if conf['complete']:
			del conf['complete']
			#send conf
			network.serverproxy.send({network.cts_new_unit:conf})
			if screen.frame.gmap.is_tile_selection_enabled:
				screen.frame.gmap.disable_tile_selection()
			

	def show_unit_conf(self,unit_type):
		'''
		proxy between unit selection and unit conf panels.
		allows gui sparkling effect or any other eye candies.
		'''
		self.conf_pan.demand(unit_type)

	def show(self):
		pass