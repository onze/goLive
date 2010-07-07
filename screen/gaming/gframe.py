
from direct.gui.DirectGui import *
from panda3d.core import ConfigVariableInt

from ..widgetwrapper import Frame
from ..layout import VLayout
from gentity import GEntity
from gmenu import GMenu
from gmap import GMap
from gnotifier import GNotifier
from gtile import GTile
from gunit import GUnit
from ..server import network

from tools import pstat

class GFrame(Frame):
	'''
	gaming frame. responsible for any display while the game is running.
	'''
	stop_gaming='stop_gaming'

	def __init__(self,*args,**kwargs):
		kwargs['layout']=VLayout
		Frame.__init__(self,*args,**kwargs)
		self.process_server_input=pstat(self.process_server_input)

	def open(self):
		'''
		frame main structure is instanciated here.
		'''
		#load all needed resources
		GMenu.load_resources()
		GMap.load_resources()
		self.menu=GMenu(parent=self,
						pref_h=50)
		#instanciate screen objects
		self.gmap=GMap(	parent=self)
		self.notifier=GNotifier(parent=self,
								pref_h=50)

	def process_server_input(self,data):
		'''
		receives server messages.
		dispatches methods calls according to server messages.
		'''
		gframe_switch={network.stc_conf:self.set_conf,
				}
		gmap_switch={network.stc_new_tile:GMap.new_tile,
				    network.stc_new_home:GMap.new_home,
				    network.stc_new_unit:GMap.new_unit,
				    }
		gunit_switch={network.stc_unit_add_path:GUnit.add_path,
					  network.stc_unit_move_over:GUnit.finish_move_to,
					  network.stc_tile_owner_change:GTile.change_owner
					 }
		for meta in data:
			if meta in gframe_switch:
				gframe_switch[meta](data[meta])
			elif meta in gmap_switch:
				gmap_switch[meta](self.gmap,data[meta])
			elif meta in gunit_switch:
				#check designed entity does exist within client
				if not 'eid' in data[meta]:
					out('ERROR in GFrame.process_server_input: eid not specified in packet.\npacket:\n'+str(data[meta]))
				if not data[meta]['eid'] in GEntity.instances:
					out('ERROR in GFrame.process_server_input: eid specified by server ('+str(data[meta]['eid'])+') does not exist client side.\npacket:\n'+str(data[meta]))	
				gunit_switch[meta](GEntity.instances[data[meta]['eid']],data[meta])
			else:
				out('WARNING in GFrame.process_server_input: packet could not get dispatched.\npacket:\n'+str(meta)+':'+str(data[meta]))
				

	def set_conf(self,conf):
		out('gframe: got config back.')
		if 'map.res' in conf:
			resx=ConfigVariableInt('map-width-'+conf['map.res']).getValue()
			resy=ConfigVariableInt('map-height-'+conf['map.res']).getValue()
			self.gmap.build_tile_matrix(conf['map.res'],resx,resy)
		else: raise Exception('in GFrame.set_conf(%s): gmap resolution not found (\'map.res\')'%str(conf))

	def start_game(self):
		'''
		'start !' animation/text/whatever
		+input handling setup
		'''
		self.menu.show()
		pass



