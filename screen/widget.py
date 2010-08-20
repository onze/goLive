
import layout

class Widget(object):
   '''base class'''
   instances=[]
   SHARED=None
   def __init__(self,x=0,y=0,w=0,h=0,*args,**kwargs):
      #print 'Widget:args=',args,'kwargs=',kwargs
      '''
      args:x,y,w,h,parent
      kwargs take precedence
      '''
      #internals
      self.children=[]
      Widget.instances.append(self)
      #default attributes
      self.x,self.y,self.w,self.h=x,y,w,h
      self._parent,self.layout=None,layout.HLayout
      self.fill=255,255,255
      self.pref_w=self.pref_h=Widget.SHARED
      #params
      if 'x' in kwargs:self.x=kwargs['x']
      if 'y' in kwargs:self.y=kwargs['y']
      if 'w' in kwargs:self.w=kwargs['w']
      if 'h' in kwargs:self.h=kwargs['h']
      if 'layout' in kwargs:self.layout=kwargs['layout']
      if 'fill' in kwargs:self.fill=kwargs['fill']
      if 'pref_w' in kwargs:self.pref_w=kwargs['pref_w']
      if 'pref_h' in kwargs:self.pref_h=kwargs['pref_h']
      if 'parent' in kwargs:self.parent=kwargs['parent']

   def __str__(self):
      return '<'+self.__class__.__name__+' pos='+str(self.pos)+',size='+str(self.size)+'>'

   def add_child(self,child):
      self.children.append(child)
      self.invalidate()

   def get_pos(self):return self.x,self.y
   def get_size(self):return self.w,self.h
   def get_parent(self):return self._parent

   def invalidate(self):
      if self.parent:self.parent.invalidate()
      else:self.validate()

   def remove_child(self,child):
      self.children.remove(child)
      self.invalidate()

   def set_pos(self,*args):
      self.x,self.y=args[0]

   def set_size(self,*args):
      self.w,self.h=args[0]
      if not self._parent:
         self.validate()

   def set_parent(self,parent):
      if self._parent:
         self._parent.remove_child(self)
      self._parent=parent
      if parent:
         self.parent.add_child(self)

   def validate(self):
      self.layout.validate(self)
      [child.validate() for child in self.children]

   pos=property(get_pos,set_pos)
   size=property(get_size,set_size)
   parent=property(get_parent,set_parent)

Frame=Spacer=Widget

class Label(Widget):
   def __init__(self,*args,**kwargs):
      #print 'Label:args=',args,'kwargs=',kwargs
      self.text=kwargs['text'] if 'text' in kwargs else 'no text'
      if not 'fill' in kwargs:kwargs['fill']=200,200,255
      Widget.__init__(self,*args,**kwargs)

#class Spacer(Widget):
#   def __init__(self,*args,**kwargs):
#      Widget.__init__(self,*args,**kwargs)
