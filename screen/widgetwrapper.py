from direct.fsm import FSM
from direct.gui.DirectGui import *
from panda3d.core import CardMaker,NodePath,PNMImage,Texture

from widget import Widget,Frame,Spacer

class WidgetWrapper(Widget):
	'''
	widget wrappers is a widget that wraps a (single) panda3d DirectGui object.
	'''
	def __init__(self,*args,**kwargs):
		self.p3dobject.reparentTo(gui)
		Widget.__init__(self,*args,**kwargs)

	#def get_parent(self):
		#return Widget.get_parent()

	def get_pos(self):
		return Widget.get_pos(self)

	def get_size(self):
		return Widget.get_size(self)

	def set_pos(self,pos):
		Widget.set_pos(self,pos)
		self.p3dobject.setPos(self.x,-1,self.y)

	def set_size(self,size):
		Widget.set_size(self,size)
		self.p3dobject.setScale(self.w,0,self.h)

	pos=property(get_pos,set_pos)
	size=property(get_size,set_size)

class Button(WidgetWrapper):
	def __init__(self,*args,**kwargs):
		if 'p3dobject' in kwargs:
			self.p3dobject=kwargs['p3dobject']
		WidgetWrapper.__init__(self,*args,**kwargs)

	def get_pos(self):
		return Widget.get_pos(self)

	def get_size(self):
		return WidgetWrapper.get_size(self)

	def set_pos(self,pos):
		Widget.set_pos(self,pos)
		dx,dy=self.parent.pos
		self.p3dobject.setPos(dx+self.x+self.w/2.,-1,dy+self.y+self.h/2.)

	def set_size(self,size):
		WidgetWrapper.set_size(self,size)
		self.p3dobject.setScale(self.w,1,self.h)

	pos=property(get_pos,set_pos)
	size=property(get_size,set_size)


class Label(WidgetWrapper):

	def __init__(self,*args,**kwargs):
		if 'text' in kwargs:
			self.text=kwargs['text']
		else:
			self.text='no text'
		Widget.__init__(self,*args,**kwargs)

	def __repr__(self):
		return ''.join(['<Label instance{text=\'',self.text,'\'}>'])

	def draw(self):
		#print self.draw,self.pos,self.size
		Widget.draw(self)
		fill(0)
		stroke(0)
		text(self.text,self.x+5,self.y+5)
