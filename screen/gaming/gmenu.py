
from direct.fsm import FSM
from direct.gui.DirectGui import DirectButton
from direct.showbase.DirectObject import DirectObject
from panda3d.core import ConfigVariableString

from screen.widgetwrapper import Frame,Button,Spacer
from screen.layout import HLayout
from server import network

class Panel(Frame):
	def __init__(self,gmenu):
		Frame.__init__(self,layout=HLayout,parent=gmenu)		
		self.gmenu=gmenu
		self.buttons=[]
		self.key_focus=[]

	def add_button(self,res,cmd,xargs,key):
		self.buttons.append(Button(	pref_w=self.gmenu.h,
										pref_h=self.gmenu.h,
										p3dobject=DirectButton(	geom=(self.gmenu.resources[res]),
																		borderWidth=(0,0),
																		command=cmd,
																		extraArgs=xargs),
										parent=self))
		self.key_focus.append(dict(key=key,cmd=cmd,xargs=xargs))
		
	def focus(self):
		'''listen to keyboard events as stocked within self.key_focus.
		panels are not responsible of their focus'''
		for d in self.key_focus:
			self.gmenu.accept(d['key']+'-up',d['cmd'],extraArgs=d['xargs'])
			
	def unfocus(self):
		'''stop listening to keyboard events (doesn't clear self.key_focus)'''
		for d in self.key_focus:
			self.gmenu.ignore(d['key'])
	
	def remove_all_buttons(self):
		for btn in self.buttons:
			btn.p3dobject.destroy()
			self.remove_child(btn)
		self.buttons=[]
		self.unfocus()
		self.key_focus=[]
		
class UnitTypePanel(Panel):
	'''presents the buttons for type of unit to select'''
	def __init__(self,gmenu):
		Panel.__init__(self,gmenu)
		self.add_button(res='type_marker',cmd=gmenu.show_unit_sel,xargs=['Type_marker'],key=self.keys['m1'])
		self.add_button(res='type_builder',cmd=gmenu.show_unit_sel,xargs=['Type_builder'],key=self.keys['m2'])
		self.add_button(res='type_fighter',cmd=gmenu.show_unit_sel,xargs=['Type_fighter'],key=self.keys['m3'])
		
	def close(self):
		self.remove_all_buttons()
		self.ignoreAll()		

class UnitSelectionPanel(Panel,FSM.FSM):
	'''presents the buttons for selection of unit to configure'''
	def __init__(self,gmenu):
		Panel.__init__(self,gmenu)
		FSM.FSM.__init__(self,'GMenu.UnitSelectionPanel')
		
	def enterBlank(self):
		'''blank state: nothing is showed.'''
		pass

	def exitBlank(self):pass
	
	def enterType_marker(self):
		self.add_button(res='zigzagger',cmd=self.gmenu.show_unit_conf,xargs=['Zigzagger'],key=self.keys['m1'])
		self.add_button(res='cw-spiraler',cmd=self.gmenu.show_unit_conf,xargs=['CwSpiraler'],key=self.keys['m2'])
		self.add_button(res='ccw-spiraler',cmd=self.gmenu.show_unit_conf,xargs=['CcwSpiraler'],key=self.keys['m3'])

	def exitType_marker(self):
		self.remove_all_buttons()
		
	
	def enterType_builder(self):
		self.add_button(res='h_sprinter',cmd=self.gmenu.show_unit_conf,xargs=['H_sprinter'],key=self.keys['m1'])
		self.add_button(res='v_sprinter',cmd=self.gmenu.show_unit_conf,xargs=['V_sprinter'],key=self.keys['m2'])
		self.add_button(res='circler',cmd=self.gmenu.show_unit_conf,xargs=['Circler'],key=self.keys['m3'])
	
	def exitType_builder(self):
		self.remove_all_buttons()
	
	def enterType_fighter(self):
		self.add_button(res='guard',cmd=self.gmenu.show_unit_conf,xargs=['Guard'],key=self.keys['m1'])
		self.add_button(res='archer',cmd=self.gmenu.show_unit_conf,xargs=['Archer'],key=self.keys['m2'])
		self.add_button(res='assassin',cmd=self.gmenu.show_unit_conf,xargs=['Assassin'],key=self.keys['m3'])
	
	def exitType_fighter(self):
		self.remove_all_buttons()
		
	def remove_all_buttons(self):
		Panel.remove_all_buttons(self)
		self.gmenu.conf_pan.request('Blank')
		
	def close(self):
		self.ignoreAll()
		self.remove_all_buttons()

class UnitConfigurationPanel(Panel,FSM.FSM):
	'''FSM presenting configuration tools for the selected unit to launch.'''
	def __init__(self,gmenu):
		Panel.__init__(self, gmenu)
		FSM.FSM.__init__(self,'GMenu.UnitConfigurationPanel')
		self._conf={}
	
	def enterBlank(self):
		'''
		blank state: nothing is showed.
		'''
		self._conf={}

	def exitBlank(self):pass	
	
	def enterClose(self):
		self._conf={}
		self.ignoreAll()
		self.remove_all_buttons()
		
	def exitClose(self):pass
	
	def remove_all_buttons(self):
		Panel.remove_all_buttons(self)
		self._conf['unit_type']=None
		gmap=screen.frame.gmap
		if gmap.is_tile_selection_enabled:
			gmap.disable_tile_selection()
		if gmap.is_unit_selection_enabled:
			gmap.disable_unit_selection()
		

	#######################################################
	#markers
	def enterZigzagger(self):
		self.add_button(res='tile-picking',cmd=screen.frame.gmap.enable_tile_selection,xargs=['single'],key=self.keys['m1'])
		self._conf['unit_type']='zizagger'
		
	def exitZigzagger(self):
		self.remove_all_buttons()
		
	def enterCwSpiraler(self):
		self.add_button(res='tile-picking',cmd=screen.frame.gmap.enable_tile_selection,xargs=['single'],key=self.keys['m1'])
		self._conf['unit_type']='cw-spiraler'
		
	def exitCwSpiraler(self):
		self.remove_all_buttons()
		
	def enterCcwSpiraler(self):
		self.add_button(res='tile-picking',cmd=screen.frame.gmap.enable_tile_selection,xargs=['single'],key=self.keys['m1'])
		self._conf['unit_type']='ccw-spiraler'
		
	def exitCcwSpiraler(self):
		self.remove_all_buttons()
	
	#######################################################
	#builders
	def enterH_sprinter(self):
		self.add_button(res='h_arrow',cmd=screen.frame.gmap.enable_tile_selection,xargs=['single'],key=self.keys['m1'])
		self._conf['unit_type']='h_sprinter'
	
	def exitH_sprinter(self):
		self.remove_all_buttons()
	
	def enterV_sprinter(self):
		self.add_button(res='v_arrow',cmd=screen.frame.gmap.enable_tile_selection,xargs=['single'],key=self.keys['m1'])
		self._conf['unit_type']='v_sprinter'
	
	def exitV_sprinter(self):
		self.remove_all_buttons()
		
	def enterCircler(self):
		self.add_button(res='tile-picking',cmd=screen.frame.gmap.enable_tile_selection,xargs=['single'],key=self.keys['m1'])
		self._conf['unit_type']='circler'

	def exitCircler(self):
		self.remove_all_buttons()
		
	#######################################################
	#fighters
	def enterGuard(self):
		self.add_button(res='wall-picking',cmd=screen.frame.gmap.enable_tile_selection,xargs=['allied-wall'],key=self.keys['m1'])
		self._conf['unit_type']='guard'

	def exitGuard(self):
		self.remove_all_buttons()

	def enterArcher(self):
		self.add_button(res='tile-picking',cmd=screen.frame.gmap.enable_tile_selection,xargs=['single'],key=self.keys['m1'])
		self._conf['unit_type']='archer'

	def exitArcher(self):
		self.remove_all_buttons()

	def enterAssassin(self):
		self.add_button(res='unit-picking',cmd=screen.frame.gmap.enable_unit_selection,xargs=['ennemy'],key=self.keys['m1'])
		self._conf['unit_type']='assassin'

	def exitAssassin(self):
		self.remove_all_buttons()
	
	#######################################################
	#misc
	
	@property
	def conf(self):
		'''
		setup a nice li'll dict containing the configuration to pass to the server.
		perfoms (half =p) a check to be (half -_-) sure the sent data won't be rejected
		'''
		self._conf['complete']=True
		if not 'unit_type' in self._conf:
			self._conf['complete']=False
		#this is for units:
		#zigzagger, cw spiraler, ccw spiraler,
		#v sprinter, h sprinter, circler
		#guard, archer
		if screen.frame.gmap.is_tile_selection_enabled:
			tiles=screen.frame.gmap.selected_tiles
			if len(tiles)>0:
				if self._conf['unit_type'] in ['zigzagger','cw-spiraler','ccw-spiraler',
														'v_sprinter','h_sprinter','circler',
														'guard','archer']:
					self._conf['x']=tiles[0].x
					self._conf['y']=tiles[0].y
			else:
				self._conf['complete']=False
		elif screen.frame.gmap.is_unit_selection_enabled:
			unit=screen.frame.gmap.selected_unit
			if unit:
				self._conf['target-eid']=unit.eid
			else:
				self._conf['complete']=False
		else:
			self._conf['complete']=False
		return self._conf

class GMenu(Frame,DirectObject):
	def __init__(self,*args,**kwargs):
		DirectObject.__init__(self)
		kwargs['fill']=165,255,121
		kwargs['layout']=HLayout
		Frame.__init__(self,*args,**kwargs)
		self.read_keys_from_config()
		#'type','unit','conf'
		self.state='type'
		self.launch_btn=Button(	pref_w=self.h*2,
										pref_h=self.h,
										p3dobject=DirectButton(	geom=(self.resources['cancel_btn']),
																		borderWidth=(0,0),
																		command=self.cancel),
										parent=self)
		self.accept(self.keys['cancel']+'-up',self.cancel)
		#graphical aspect: [cancel_btn | unit_type_panel | unit_selection_panel | unit_configuration_panel | launch_btn]
		self.type_pan=UnitTypePanel(self)
		self.type_pan.focus()
		self.sel_pan=UnitSelectionPanel(self)
		self.sel_pan.request('Blank')
		self.conf_pan=UnitConfigurationPanel(self)
		self.conf_pan.request('Blank')
		Spacer(parent=self)
		self.launch_btn=Button(	pref_w=self.h*2,
							    pref_h=self.h,
								p3dobject=DirectButton(geom=(self.resources['launch_btn']),
														borderWidth=(0,0),
														command=self.launch_unit),
								parent=self)
		self.accept('enter-up',self.launch_unit)
		self.accept(self.keys['launch']+'-up',self.launch_unit)
		self.accept('mouse3-up',self.launch_unit)
	
	@staticmethod
	def load_resources():
		#load resources
		unit_type_sel_res=loader.loadModel('data/gui/gmenu/unit_types_btn.egg')
		unit_sel_res=loader.loadModel('data/gui/gmenu/units_btn.egg')
		unit_conf_res=loader.loadModel('data/gui/gmenu/unit_conf.egg')
		misc_res=loader.loadModel('data/gui/gmenu/gmenu_misc.egg')
		GMenu.resources={#types
							'type_marker':unit_type_sel_res.find('**/type.markers'),
							'type_builder':unit_type_sel_res.find('**/type.builders'),
							'type_fighter':unit_type_sel_res.find('**/type.fighters'),
							#units
							#markers
							'zigzagger':unit_sel_res.find('**/zigzagger'),
							'cw-spiraler':unit_sel_res.find('**/cw-spiraler'),
							'ccw-spiraler':unit_sel_res.find('**/ccw-spiraler'),
							'circler':unit_sel_res.find('**/circler'),
							#builders
							'h_sprinter':unit_sel_res.find('**/h_sprinter'),
							'v_sprinter':unit_sel_res.find('**/v_sprinter'),
							#fighters
							'guard':unit_sel_res.find('**/guard'),
							'archer':unit_sel_res.find('**/archer'),
							'assassin':unit_sel_res.find('**/assassin'),
							#conf stuff
							'tile-picking':unit_conf_res.find('**/tile-picking'),
							'wall-picking':unit_conf_res.find('**/wall-picking'),
							'unit-picking':unit_conf_res.find('**/unit-picking'),
							'h_arrow':unit_conf_res.find('**/h_arrow'),
							'v_arrow':unit_conf_res.find('**/v_arrow'),
							'launch_btn':misc_res.find('**/launch_btn'),
							'cancel_btn':misc_res.find('**/cancel_btn'),
							}
		for k in GMenu.resources:
			if GMenu.resources[k]==None:
				raise Exception('could not load GMenu.resource \''+k+'\'')
	
	def cancel(self):
		if self.state=='type':
			pass
		elif self.state=='unit':
			self.sel_pan.close()
			self.type_pan.focus()
			self.state='type'
		elif self.state=='conf':
			self.conf_pan.demand('Close')
			self.sel_pan.focus()
			self.state='unit'

	def close(self):
		self.conf_pan.demand('Close')
		self.sel_pan.close()
		self.type_pan.close()

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
			gmap=screen.frame.gmap
			self.state='type'
			self.conf_pan.demand('Close')
			self.sel_pan.close()
			self.type_pan.focus()
			self.state='unit'
			if gmap.is_tile_selection_enabled:
				gmap.disable_tile_selection()
			if gmap.is_unit_selection_enabled:
				gmap.disable_unit_selection()

	def read_keys_from_config(self):
		Panel.keys=self.keys={	'm1':ConfigVariableString('gmenu-m1').getValue(),
										'm2':ConfigVariableString('gmenu-m2').getValue(),
										'm3':ConfigVariableString('gmenu-m3').getValue(),
										'launch':ConfigVariableString('gmenu-launch').getValue(),
										'cancel':ConfigVariableString('gmenu-cancel').getValue(),
									}

	def show_unit_sel(self,unit_type):
		'''
		proxy between unit type selection and unit selection panels.
		allows gui sparkling effect or any other eye candies.
		'''
		self.type_pan.unfocus()
		self.state='unit'
		self.sel_pan.demand(unit_type)
		self.sel_pan.focus()

	def show_unit_conf(self,unit_type):
		'''
		proxy between unit selection and unit conf panels.
		allows gui sparkling effect or any other eye candies.
		'''
		self.sel_pan.unfocus()
		self.state='conf'
		self.conf_pan.demand(unit_type)
		self.conf_pan.focus()

	def show(self):
		pass