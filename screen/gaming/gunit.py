
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import LerpPosInterval
from panda3d.core import ConfigVariableInt

from gentity import GEntity

class GUnit(GEntity):
	
	def __init__(self,conf):
		GEntity.__init__(self,conf)
		self.p3dobject.reparentTo(self.gmap.root)
		self.p3dobject.setPos(self.gmap.root.find('**/tile_'+str(conf['tileid'])),0,0,0)
		self.target_tile=None
		
	def __del__(self):
		GEntity.__del__(self)
		
	def move_to(self,data):
		'''
		starts a move toward the given tile.
		data={eid:unit eid,
		start:tile at start of move,
		end:tile at end of move,
		begin:frame at which to start the move,
		frames:number of frame dedicated to the move}
		'''
		#check for data completeness
		warning_intro='WARNING in GUnit.move_to: '
		for tag in ['start','end','begin','frames']:
			if not tag in data:
				out(warning_intro+'incomplete data misses tag \''+tag+'\'.\ndata:\n'+str(data))
				return
		#check for validity
		if not data['start'] in self.instances:
			out(warning_intro+'starting tile not found.\ndata:\n'+str(data))
			return
		if not data['end'] in self.instances:
			out(warning_intro+'ending tile not found.\ndata:\n'+str(data))
			return
		#data considered valid
		self.move_frame=data['begin']
		self.move_interval=LerpPosInterval(self.p3dobject,
										   data['frames']/float(ConfigVariableInt('clock-frame-rate').getValue()),
										   self.instances[data['end']].p3dobject.getPos(),
										   startPos=self.instances[data['start']].p3dobject.getPos(),
										   name='interval_unit_move_'+str(self.eid)
										   )
		update_list.append(self.update_move)
		out('GUnit.move_to:'+str(data))
		out( _from=str(self.instances[data['start']].p3dobject.getPos()),
			 _to=str(self.instances[data['end']].p3dobject.getPos()),
			 _duration=str(data['frames']/float(ConfigVariableInt('clock-frame-rate').getValue())),
			 _currentPos=str(self.p3dobject.getPos())
			 )
		
	def update_move(self):
#		out('GUnit.update',move_frame=self.move_frame,frame_no=self.frame_no)
		t=self.move_interval.getT()
		d=self.move_interval.getDuration()
#		out('client '+str(t*100./d)+'%')
		if self.move_interval.isPlaying() and d-t<.05:
			render.analyze()
			update_list.remove(self.update_move)
		if self.move_frame<=self.frame_no and not self.move_interval.isPlaying():
				self.move_interval.start()
		
class GH_Sprinter(GUnit):
	def __init__(self,conf):
		self.p3dobject=Actor('data/models/units/v_sprinter.egg',
							 {'run':'data/models/units/v_sprinter-run.egg',
							  }
							 )
		GUnit.__init__(self,conf)
#		home.setH(tools.random([0,90,180,270]))
		
class GV_Sprinter(GUnit):
	def __init__(self,conf):
		self.p3dobject=Actor('data/models/units/v_sprinter.egg',
							 {'run':'data/models/units/v_sprinter-run.egg',
							  }
							 )
		GUnit.__init__(self,conf)
#		home.setH(tools.random([0,90,180,270]))