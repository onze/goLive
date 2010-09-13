# -*- coding: utf-8 -*-

from eventProducer import eventProducer

class Leaf:
   def __init__(self,x,y,data):
      self.x,self.y,self.data=x,y,data
   def __str__(self):
      return 'leaf[%f,%f]:%s'%(self.x,self.y,str(self.data))

class QuadTree(eventProducer):
   def __init__(self,x=0,y=0,width=0,height=0):
      eventProducer.__init__(self)
      self.add_event('new_node')
      self.add_event('new_leaf')
      self.x,self.y=x,y
      self.width,self.height=width,height
      #0 sw,1 se,2 ne,3 nw
      self.children=[None]*4

   def __str__(self):
      s=['node[%f,%f]'%(self.x,self.y)+'\n<']
      #for i,child in enumerate([c[3],c[2],c[0],c[1]]):
      s.extend([str(child) for child in self.children])
      s.append('>')
      return '\n'.join(s)

   def add(self,x,y,data):
      '''
      returns the quadtree that directly contains the inserted data.
      raises an exception if x,y is out of bound
      '''
      print '----'
      print 'add(%i,%i) to %ix%i located at %i,%i'%(x,y,self.width,self.height,self.x,self.y)
      xinbound=self.x-self.width/2.<=x<=self.x+self.width/2.
      yinbound=self.y-self.height/2.<=y<=self.y+self.height/2.
      if not (xinbound and yinbound):
         print xinbound,':',self.x-self.width/2.<=x,' and ',x<=self.x+self.width/2.
         print yinbound,':',self.y-self.height/2.<=y,' and ',y<=self.y+self.height/2.
         raise Exception('data location (%i,%i) is out of bound %ix%i located at %i,%i'%(x,y,self.width,self.height,self.x,self.y))
      index=int(x>self.x)+2*int(y>self.y)
      print 'x>self.x:',x>self.x
      print 'y>self.y:',y>self.y
      print 'index:',index
      child=self.children[index]
      if child==None:
         #free slot
         self.children[index]=Leaf(x,y,data)
         self.trigger_event('new_leaf',leaf=self.children[index],parent_node=self)
         return self
      elif isinstance(child,QuadTree):
         #child can process adding itself
         return child.add(x,y,data)
      else:
         #slot is occupied by a leaf
         save=self.children[index]
         #0 sw,1 se,2 ne,3 nw
         nx,ny={  0:(self.x-self.width/4.,self.y-self.height/4.),
                  1:(self.x+self.width/4.,self.y-self.height/4.),
                  2:(self.x-self.width/4.,self.y+self.height/4.),
                  3:(self.x+self.width/4.,self.y+self.height/4.)
               }[index]
         #nx,ny=(save.x+x)/2.,(save.y+y)/2.
         print 'splitting at %s/%s (%sx%s)'%(str(nx),str(ny),str(self.width/2.),str(self.height/2))
         self.children[index]=QuadTree(nx,ny,self.width/2.,self.height/2.)
         self.trigger_event('new_node',node=self.children[index],parent=self,old_leaf=save)
         self.children[index].add(save.x,save.y,save.data)
         return self.children[index].add(x,y,data)
   
   def child_by_dir(self,dir):
      return self.children[{'sw':0,'se':1,'ne':2,'nw':3}[dir]]


