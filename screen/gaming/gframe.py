
from direct.gui.DirectGui import *
from panda3d.core import ConfigVariableInt

from ..widgetwrapper import Frame
from ..layout import VLayout
from gmenu import GMenu
from gmap import GMap
from gnotifier import GNotifier
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
		gmap_switch={network.stc_tile_sync:GMap.sync_tile,
				    network.stc_newhome:GMap.new_home,
				    network.stc_new_unit:GMap.new_unit,
				    }
		gentity_switch={network.stc_unit_moving:GUnit.move_to,
					 }
		for meta in data:
			if meta in gframe_switch:
				gframe_switch[meta](data[meta])
			elif meta in gmap_switch:
				gmap_switch[meta](self.gmap,data[meta])
			elif meta in gentity_switch:
				#check designed entity does exist within client
				if not 'eid' in data[meta]:
					out('ERROR in GFrame.process_server_input: eid not specified in packet.\npacket:\n'+str(meta))
				if not data[meta]['eid'] in self.gmap.entities:
					out('ERROR in GFrame.process_server_input: eid specified by server ('+data[meta]['eid']+') does not exist client side.\npacket:\n'+str(meta))
				gentity_switch[meta](self.gmap.entities[data[meta]['eid']],data[meta])
			elif not meta=='frame_no':
				out('WARNING in GFrame.process_server_input: meta \''+str(meta)+'\' could not be dispatched.\npacket:\n'+str(data))
				

	def set_conf(self,conf):
		out('gframe: got config back.')
		if 'map.res' in conf:
			resx=ConfigVariableInt('map-width-'+conf['map.res']).getValue()
			resy=ConfigVariableInt('map-height-'+conf['map.res']).getValue()
			self.gmap.build_tile_matrix(resx,resy)
		else: raise Exception('in GFrame.set_conf(%s): gmap resolution not found (\'map.res\')'%str(conf))

	def start_game(self):
		'''
		'start !' animation/text/whatever
		+input handling setup
		'''
		self.menu.show()
		pass



