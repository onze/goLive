
from direct.fsm import FSM
from direct.gui.DirectGui import DirectButton
from direct.showbase.DirectObject import DirectObject

from screen.widgetwrapper import Frame,Button,Spacer
from screen.layout import HLayout
from server import network

class Panel(Frame):
	def __init__(self,gmenu):
		Frame.__init__(self,layout=HLayout,parent=gmenu)		
		self.gmenu=gmenu
		
class UnitTypePanel(Panel):
	'''presents the buttons for type of unit to select'''
	def __init__(self,gmenu):
		Panel.__init__(self,gmenu)
		self.marker_btn=Button(pref_w=gmenu.h,
									pref_h=gmenu.h,
									p3dobject=DirectButton(geom=(gmenu.resources['type_marker']),
																borderWidth=(0,0),
																command=gmenu.show_unit_sel,
																extraArgs=['Type_marker']),
									parent=self) 
		self.builder_btn=Button(	pref_w=gmenu.h,
									pref_h=gmenu.h,
									p3dobject=DirectButton(geom=(gmenu.resources['type_builder']),
															borderWidth=(0,0),
															command=gmenu.show_unit_sel,
															extraArgs=['Type_builder']),
								parent=self) 
		self.fighter_btn=Button(	pref_w=gmenu.h,
									pref_h=gmenu.h,
									p3dobject=DirectButton(geom=(gmenu.resources['type_fighter']),
															borderWidth=(0,0),
															command=gmenu.show_unit_sel,
															extraArgs=['Type_fighter']),
								parent=self)
		gmenu.accept('q',gmenu.show_unit_sel,extraArgs=['Type_marker'])
		gmenu.accept('w',gmenu.show_unit_sel,extraArgs=['Type_builder'])
		gmenu.accept('e',gmenu.show_unit_sel,extraArgs=['Type_fighter'])
		
	def close(self):
		self.ignoreAll()
		self.marker_btn.p3dobject.destroy()
		self.remove_child(self.marker_btn)
		del self.marker_btn
		self.builder_btn.p3dobject.destroy()
		self.remove_child(self.builder_btn)
		del self.builder_btn
		self.fighter_btn.p3dobject.destroy()
		self.remove_child(self.fighter_btn)
		del self.fighter_btn

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
		self.zigzagger_btn=Button(	pref_w=self.gmenu.h,
								    pref_h=self.gmenu.h,
									p3dobject=DirectButton(geom=(self.gmenu.resources['zigzagger']),
															borderWidth=(0,0),
															command=self.gmenu.show_unit_conf,
															extraArgs=['Zigzagger']),
									parent=self)
		self.spiraler_btn=Button(	pref_w=self.gmenu.h,
								    pref_h=self.gmenu.h,
									p3dobject=DirectButton(geom=(self.gmenu.resources['spiraler']),
															borderWidth=(0,0),
															command=self.gmenu.show_unit_conf,
															extraArgs=['Spiraler']),
									parent=self)
		self.gmenu.accept('a',self.gmenu.show_unit_conf,extraArgs=['Zigzagger'])
		self.gmenu.accept('s',self.gmenu.show_unit_conf,extraArgs=['Spiraler'])

	def exitType_marker(self):
		self.gmenu.ignore('a')
		self.gmenu.ignore('s')
		self.zigzagger_btn.p3dobject.destroy()
		self.remove_child(self.zigzagger_btn)
		del self.zigzagger_btn
		self.spiraler_btn.p3dobject.destroy()
		self.remove_child(self.spiraler_btn)
		del self.spiraler_btn
		
	
	def enterType_builder(self):
		self.h_sprinter_btn=Button(	pref_w=self.gmenu.h,
								    pref_h=self.gmenu.h,
									p3dobject=DirectButton(geom=(self.gmenu.resources['h_sprinter']),
															borderWidth=(0,0),
															command=self.gmenu.show_unit_conf,
															extraArgs=['H_sprinter']),
									parent=self) 
		self.v_sprinter_btn=Button(	pref_w=self.gmenu.h,
									pref_h=self.gmenu.h,
									p3dobject=DirectButton(geom=(self.gmenu.resources['v_sprinter']),
															borderWidth=(0,0),
															command=self.gmenu.show_unit_conf,
															extraArgs=['V_sprinter']),
								parent=self)
		self.circler_btn=Button(	pref_w=self.gmenu.h,
									pref_h=self.gmenu.h,
									p3dobject=DirectButton(geom=(self.gmenu.resources['circler']),
															borderWidth=(0,0),
															command=self.gmenu.show_unit_conf,
															extraArgs=['Circler']),
								parent=self)
		self.gmenu.accept('a',self.gmenu.show_unit_conf,extraArgs=['H_sprinter'])
		self.gmenu.accept('s',self.gmenu.show_unit_conf,extraArgs=['V_sprinter'])
		self.gmenu.accept('d',self.gmenu.show_unit_conf,extraArgs=['Circler'])
	
	def exitType_builder(self):
		self.gmenu.ignore('a')
		self.gmenu.ignore('s')
		self.gmenu.ignore('d')
		self.h_sprinter_btn.p3dobject.destroy()
		self.remove_child(self.h_sprinter_btn)
		del self.h_sprinter_btn
		self.v_sprinter_btn.p3dobject.destroy()
		self.remove_child(self.v_sprinter_btn)
		del self.v_sprinter_btn
		self.circler_btn.p3dobject.destroy()
		self.remove_child(self.circler_btn)
		del self.circler_btn
	
	def enterType_fighter(self):
		self.guard_btn=Button(	pref_w=self.gmenu.h,
								    pref_h=self.gmenu.h,
									p3dobject=DirectButton(geom=(self.gmenu.resources['guard']),
															borderWidth=(0,0),
															command=self.gmenu.show_unit_conf,
															extraArgs=['Guard']),
									parent=self)
		self.archer_btn=Button(	pref_w=self.gmenu.h,
								    pref_h=self.gmenu.h,
									p3dobject=DirectButton(geom=(self.gmenu.resources['archer']),
															borderWidth=(0,0),
															command=self.gmenu.show_unit_conf,
															extraArgs=['Archer']),
									parent=self)
		self.assassin_btn=Button(	pref_w=self.gmenu.h,
								    pref_h=self.gmenu.h,
									p3dobject=DirectButton(geom=(self.gmenu.resources['assassin']),
															borderWidth=(0,0),
															command=self.gmenu.show_unit_conf,
															extraArgs=['Assassin']),
									parent=self)
		self.gmenu.accept('a',self.gmenu.show_unit_conf,extraArgs=['Guard'])
		self.gmenu.accept('s',self.gmenu.show_unit_conf,extraArgs=['Archer'])
		self.gmenu.accept('d',self.gmenu.show_unit_conf,extraArgs=['Assassin'])
	
	def exitType_fighter(self):
		self.gmenu.ignore('a')
		self.gmenu.ignore('s')
		self.gmenu.ignore('d')
		self.guard_btn.p3dobject.destroy()
		self.remove_child(self.guard_btn)
		del self.guard_btn
		self.archer_btn.p3dobject.destroy()
		self.remove_child(self.archer_btn)
		del self.archer_btn
		self.assassin_btn.p3dobject.destroy()
		self.remove_child(self.assassin_btn)
		del self.assassin_btn
		
	def close(self):
		self.ignoreAll()

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
		del self._conf
		self.ignoreAll()
		
	def exitClose(self):pass

	#######################################################
	#markers
	def enterZigzagger(self):
		self.tile_picking_btn=Button(	pref_w=self.gmenu.h,
						    pref_h=self.gmenu.h,
							p3dobject=DirectButton(geom=(self.gmenu.resources['tile-picking']),
													borderWidth=(0,0),
													command=screen.frame.gmap.enable_tile_selection,
													extraArgs=['single']),
							parent=self)
		self.accept('z',screen.frame.gmap.enable_tile_selection, extraArgs=['single'])
		self._conf['unit_type']='zizagger'
		
	def exitZigzagger(self):
		if screen.frame.gmap.is_tile_selection_enabled:
			screen.frame.gmap.disable_tile_selection()
		self.remove_child(self.tile_picking_btn)
		self.tile_picking_btn.p3dobject.destroy()
		del self.tile_picking_btn
		self._conf['unit_type']=None
		
	def enterSpiraler(self):
		self.tile_picking_btn=Button(	pref_w=self.gmenu.h,
						    pref_h=self.gmenu.h,
							p3dobject=DirectButton(geom=(self.gmenu.resources['tile-picking']),
													borderWidth=(0,0),
													command=screen.frame.gmap.enable_tile_selection,
													extraArgs=['single']),
							parent=self)
		self.accept('z',screen.frame.gmap.enable_tile_selection, extraArgs=['single'])
		self._conf['unit_type']='spiraler'
		
	def exitSpiraler(self):
		if screen.frame.gmap.is_tile_selection_enabled:
			screen.frame.gmap.disable_tile_selection()
		self.remove_child(self.tile_picking_btn)
		self.tile_picking_btn.p3dobject.destroy()
		del self.tile_picking_btn
		self._conf['unit_type']=None
	
	#######################################################
	#builders
	def enterH_sprinter(self):
		'''
		will display hsprinter conf buttons
		'''
		self.arrow=Button(	pref_w=self.gmenu.h,
						    pref_h=self.gmenu.h,
							p3dobject=DirectButton(geom=(self.gmenu.resources['h_arrow']),
													borderWidth=(0,0),
													command=screen.frame.gmap.enable_tile_selection,
													extraArgs=['single']),
							parent=self)
		self.accept('z',screen.frame.gmap.enable_tile_selection, extraArgs=['single'])
		self._conf['unit_type']='h_sprinter'
	
	def exitH_sprinter(self):
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
		self.arrow=Button(	pref_w=self.gmenu.h,
						    pref_h=self.gmenu.h,
							p3dobject=DirectButton(geom=(self.gmenu.resources['v_arrow']),
													borderWidth=(0,0),
													command=screen.frame.gmap.enable_tile_selection,
													extraArgs=['single']),
							parent=self)
		self.accept('z',screen.frame.gmap.enable_tile_selection, extraArgs=['single'])
		self._conf['unit_type']='v_sprinter'
	
	def exitV_sprinter(self):
		if screen.frame.gmap.is_tile_selection_enabled:
			screen.frame.gmap.disable_tile_selection()
		self.remove_child(self.arrow)
		self.arrow.p3dobject.destroy()
		del self.arrow
		self._conf['unit_type']=None
		
	def enterCircler(self):
		self.tile_picking_btn=Button(	pref_w=self.gmenu.h,
						    pref_h=self.gmenu.h,
							p3dobject=DirectButton(geom=(self.gmenu.resources['tile-picking']),
													borderWidth=(0,0),
													command=screen.frame.gmap.enable_tile_selection,
													extraArgs=['single']),
							parent=self)
		self.accept('z',screen.frame.gmap.enable_tile_selection, extraArgs=['single'])
		self._conf['unit_type']='circler'

	def exitCircler(self):
		if screen.frame.gmap.is_tile_selection_enabled:
			screen.frame.gmap.disable_tile_selection()
		self.remove_child(self.tile_picking_btn)
		self.tile_picking_btn.p3dobject.destroy()
		del self.tile_picking_btn
		self._conf['unit_type']=None
		
	#######################################################
	#fighters
	def enterGuard(self):pass
	def exitGuard(self):pass
	def enterArcher(self):
		self.tile_picking_btn=Button(	pref_w=self.gmenu.h,
						    pref_h=self.gmenu.h,
							p3dobject=DirectButton(geom=(self.gmenu.resources['tile-picking']),
													borderWidth=(0,0),
													command=screen.frame.gmap.enable_tile_selection,
													extraArgs=['single']),
							parent=self)
		self.accept('z',screen.frame.gmap.enable_tile_selection, extraArgs=['single'])
		self._conf['unit_type']='archer'

	def exitArcher(self):
		if screen.frame.gmap.is_tile_selection_enabled:
			screen.frame.gmap.disable_tile_selection()
		self.remove_child(self.tile_picking_btn)
		self.tile_picking_btn.p3dobject.destroy()
		del self.tile_picking_btn
		self._conf['unit_type']=None

	def enterAssassin(self):pass
	def exitAssassin(self):pass
	
	
	#######################################################
	#misc
	
	@property
	def conf(self):
		'''
		setup a nice li'll dict containing the configuration to pass to the server.
		'''
		self._conf['complete']=True
		if not 'unit_type' in self._conf:
			self._conf['complete']=False
		if screen.frame.gmap.is_tile_selection_enabled:
			tiles=screen.frame.gmap.selected_tiles
			if len(tiles)>0:
				if self._conf['unit_type'] in ['v_sprinter','h_sprinter']:
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
		kwargs['layout']=HLayout
		Frame.__init__(self,*args,**kwargs)
		#graphical aspect: [unit_type_panel | unit_selection_panel | unit_configuration_panel | launch_btn]
		self.type_pan=UnitTypePanel(self)
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
		self.accept('enter',self.launch_unit)
		self.accept('space',self.launch_unit)
		self.accept('mouse3',self.launch_unit)
	
	@staticmethod
	def load_resources():
		#load resources
		unit_type_sel_res=loader.loadModel('data/gui/gmenu/unit_types_btn.egg')
		unit_sel_res=loader.loadModel('data/gui/gmenu/units_btn.egg')
		unit_conf_res=loader.loadModel('data/gui/gmenu/unit_conf.egg')
		launch_btn_res=loader.loadModel('data/gui/gmenu/launch_btn.egg')
		GMenu.resources={#types
							'type_marker':unit_type_sel_res.find('**/type.markers'),
							'type_builder':unit_type_sel_res.find('**/type.builders'),
							'type_fighter':unit_type_sel_res.find('**/type.fighters'),
							#units
							#markers
							'zigzagger':unit_sel_res.find('**/zigzagger'),
							'spiraler':unit_sel_res.find('**/spiraler'),
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
							'h_arrow':unit_conf_res.find('**/h_arrow'),
							'v_arrow':unit_conf_res.find('**/v_arrow'),
							'launch_btn':launch_btn_res.find('**/launch_btn'),
							}
		for k in GMenu.resources:
			print k,GMenu.resources[k]
			if GMenu.resources[k]==None:
				raise Exception('could not load GMenu.resource \''+k+'\'')

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

	def show_unit_sel(self,unit_type):
		'''
		proxy between unit type selection and unit selection panels.
		allows gui sparkling effect or any other eye candies.
		'''
		self.sel_pan.demand(unit_type)
			

	def show_unit_conf(self,unit_type):
		'''
		proxy between unit selection and unit conf panels.
		allows gui sparkling effect or any other eye candies.
		'''
		self.conf_pan.demand(unit_type)

	def show(self):
		pass