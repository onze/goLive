
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import LerpPosInterval,Func,Sequence
from panda3d.core import ConfigVariableInt

from gentity import GEntity
from tools import dist3

class GUnit(GEntity):
	
	def __init__(self,conf):
		GEntity.__init__(self,conf)
		self.p3dobject.reparentTo(self.gmap.root)
		self.p3dobject.setPos(self.gmap.root.find('**/tile_'+str(conf['tileid'])),0,0,0)
		#supposedly already a float, but will screw up if not, so just making sure.
		self.move_speed=float(conf['move_speed'])
		self.path=[]
		self.popout_when_move_over=False
		
	def dispose(self):
		'''del method'''
		GEntity.dispose(self)
		self.popout_sequence.finish()
		del self.popout_sequence

	def add_path(self,data):
		'''
		adds tile to pass by.
		'''
		#check for data completeness
		if not 'path' in data:
			out('WARNING in GUnit.add_path: incomplete data:\n'+str(data))
			return
		elif not isinstance(data['path'],list):
			out('WARNING in GUnit.add_path: invalid data:\n'+str(data))
			return
		#data considered valid
		self.path.extend([self.instances[eid] for eid in data['path']])
		if not self.update_move in update_list: 
			update_list.append(self.update_move)
		#out('GUnit.add_path:'+str(data))
	
	def finish_move_to(self,data):
		'''triggered by server side unit, to indicate the need to popout at end of move.'''
		out('GUnit.finish_move_to()'+str(data))
		if self.update_move in update_list:
			self.popout_when_move_over=True
		else:
			self.popout()
			
	def popout(self):
		'''sets up the popout animation'''
		scale=self.p3dobject.scaleInterval(.5,(.1,.1,.1))
		finish=Func(lambda:dispose_list.append(self))
		self.popout_sequence=Sequence(scale,finish)
		self.popout_sequence.start()
		
	def update_move(self):
		'''called every frame during while a move.'''
		if len(self.path)==0:
			out('WARNING in GUnit.update_move: path is empty, but method still called. removing it.')
			update_list.remove(self.update_move)
			return
		if not hasattr(self,'move_interval'):
			#start moving
			#first 3 args=model,duration,pos, the duration=1/... is relative to server side tile side size
			self.move_interval=LerpPosInterval(self.p3dobject,
											   (1/(self.move_speed*float(ConfigVariableInt('clock-frame-rate').getValue()))),
											   self.path[0].p3dobject.getPos(),
											   name='interval_unit_move_'+str(self.eid)
											   )
			self.p3dobject.lookAt(self.path[0].p3dobject.getPos())
			self.p3dobject.loop('run')
			self.move_interval.start()
		else:
			#is move ~over ?
			#t=self.move_interval.getT()
			#d=self.move_interval.getDuration()
			#d=d-t
			d=dist3(self.p3dobject,self.path[0].p3dobject)
			#out('client '+str(t*100./d)+'%')
	        #arrived
			if d<self.move_speed:
				#out('client '+str(self.path[0].eid)+'@'+str(self.frame_no))
				self.p3dobject.setPos(self.path[0].p3dobject,0,0,0)
				self.path.pop(0)
				if len(self.path)==0:
					self.p3dobject.stop()
					self.move_interval.finish()
					del self.move_interval
					update_list.remove(self.update_move)
					if self.popout_when_move_over:
						self.popout()
				else:
					#first 3 args=model,duration,pos
					self.move_interval.finish()
					self.move_interval=LerpPosInterval(self.p3dobject,
													   (1/(self.move_speed*float(ConfigVariableInt('clock-frame-rate').getValue()))),
													   self.path[0].p3dobject.getPos(),
													   name='interval_unit_move_'+str(self.eid)
													   )
					self.p3dobject.lookAt(self.path[0].p3dobject.getPos())
					self.move_interval.start()
				
		
class GH_Sprinter(GUnit):
	def __init__(self,conf):
		self.p3dobject=Actor('data/models/units/v_sprinter.egg',
							 {'run':'data/models/units/v_sprinter-run.egg',
							  }
							 )
		GUnit.__init__(self,conf)
		#home.setH(tools.random([0,90,180,270]))

		
class GV_Sprinter(GUnit):
	def __init__(self,conf):
		self.p3dobject=Actor('data/models/units/v_sprinter.egg',
							 {'run':'data/models/units/v_sprinter-run.egg',
							  }
							 )
		GUnit.__init__(self,conf)
		#home.setH(tools.random([0,90,180,270]))