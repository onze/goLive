
#from direct.gui.DirectGui import base
from direct.showbase.DirectObject import DirectObject
from panda3d.core import ConfigVariableString
from panda3d.core import PandaNode,NodePath
from panda3d.core import CollisionTraverser,CollisionNode,Vec3
from panda3d.core import CollisionHandlerQueue,CollisionRay
from pandac.PandaModules import GeomNode
from server import network

class GamingCam(object,DirectObject):
   yshift,zshift=5,5
   ymin,ymax=10,70
   zmin,zmax=10,70
   zoom_speed=.1
   move_speed=.5
   def __init__(self,gmap,gaming_zone):
      DirectObject.__init__(self)
      #gaming zone (used for mouse movement), as a tools.Rectangle
      self.gaming_zone=gaming_zone
      #actual camera node
      self.p3dcam=base.camera
      #what the cam is oriented to
      self._target=base.render.attachNewNode('GaminCam.target')
      #range=[0,1] between min and max closeness to ground
      self.level=.7
      #
      #keys_down acts as a pool containing keys (+mouse buttons) currently down
      self.keys_down=[]
      update_list.append(self.update)
      #setup for mouse picking
      picker_node=CollisionNode('gcam_to_mouse_ray')#general collision node
      picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
      self.picker_ray=CollisionRay()#solid ray to attach to coll node
      picker_node.addSolid(self.picker_ray)
      self.picker_np=self.p3dcam.attachNewNode(picker_node)#attach this node to gcam
      self.collision_queue=CollisionHandlerQueue()#stores collisions
      self.collision_traverser=CollisionTraverser('gcam_traverser')#actual computer
      self.collision_traverser.addCollider(self.picker_np,self.collision_queue)
      base.cTrav=self.collision_traverser
      self.gmap=gmap
      #stack of states (state=pos+zoom)
      self.states_stack=[]
      #enable the cam to move according to keyboard and mouse
      self.move_enabled=True

   def __del__(self):
      update_list.remove(self.update)
      self.ignoreAll()
      
   def center(self):
      self._target.setPos(0,0,0)
      
   def disable_move(self):
      self.move_enabled=False

   def enable_move(self):
      self.move_enabled=True

   def get_level(self):
      return self._level
   
   def get_picked_tile(self):
      '''
      returns
      '''
      if base.mouseWatcherNode.hasMouse():
         #get the mouse position
         mpos = base.mouseWatcherNode.getMouse()
         #Set the position of the ray based on the mouse position
#         self.picker_ray.setFromLens(self.p3dcam.node().getLens(), mpos.getX(), mpos.getY())
         self.picker_ray.setFromLens(base.camNode, mpos.getX(), mpos.getY())
         self.collision_traverser.traverse(self.gmap.tile_matrix_node)
         if self.collision_queue.getNumEntries()>0:
            #useless since collision test is done against a single object
            self.collision_queue.sortEntries()
            entry=self.collision_queue.getEntry(0)
            x,y,_=entry.getSurfacePoint(self.gmap.tile_matrix_node)
            x=(x+self.gmap.resx)/2.
            y=(y+self.gmap.resy)/2.
            x=max(x,0)
            x=min(x,self.gmap.resx)
            y=max(y,0)
            y=min(y,self.gmap.resy)
            x=int(x)
            y=int(y)
            #out(pos=(x,y,z))
            return self.gmap.tile_matrix[x][y]
      return None
   
   def get_picked_unit(self):
      if base.mouseWatcherNode.hasMouse():
         #get the mouse position
         mpos = base.mouseWatcherNode.getMouse()
         #Set the position of the ray based on the mouse position
#         self.picker_ray.setFromLens(self.p3dcam.node().getLens(), mpos.getX(), mpos.getY())
         self.picker_ray.setFromLens(base.camNode, mpos.getX(), mpos.getY())
         self.collision_traverser.traverse(self.gmap.units_node)
         if self.collision_queue.getNumEntries()>0:
            #useless since collision test is done against a single object
            self.collision_queue.sortEntries()
            entry=self.collision_queue.getEntry(0)
            return entry.getIntoNodePath().findNetTag('GUnit-pickable')
      return None
      

   def get_target(self):
      return self._target
   
   def mouse_up(self,btn):
      if btn=='left':
         target=self.get_picked_tile()
         out(target)
         if target:
            network.serverproxy.send({network.cts_dbg_dump_entity:{'eid':target.eid}})
      elif btn=='middle':
         self.set_level(.7)
         self.set_target(Vec3(0,-9,0))

   def move(self,dx=0,dy=0):
      self._target.setPos(self._target,dx,dy,0)
      self.update_cam()

   def push_state(self):
      out('GCam.push_state()')
      pos,zoom=self._target.getPos(),self.level
      self.states_stack.append((pos,zoom))
      
   def pop_state(self):
      out('GCam.pop_state()')
      pos,zoom=self.states_stack.pop(-1)
      self._target.setPos(*pos)
      self.level=zoom
      self.update_cam()

   def set_level(self,level):
      self._level=level
      self.update_cam()

   def set_target(self,target):
      '''
      make the cam look at the given target.
      target can be a set of coordinates, or a node/nodepath.
      '''
      if isinstance(target,PandaNode) or isinstance(target,NodePath):
         self._target.setPos(target,0,0,0)
      if isinstance(target,tuple):
         self._target.setPos(Vec3(*target))
      else:
         self._target.setPos(target)
      self.update_cam()

   def start_accepting(self):
      '''
      the gaming cam is created at gmap creation, so it has to wait
      until all data structures are created before accepting events.
      '''
      self.accept(ConfigVariableString('key-cam-zoom-in').getValue()+'-up',self.zoom,extraArgs=[-GamingCam.zoom_speed])
      self.accept(ConfigVariableString('key-cam-zoom-out').getValue()+'-up',self.zoom,extraArgs=[GamingCam.zoom_speed])
      self.accept(ConfigVariableString('key-cam-right').getValue(),self.keys_down.append,extraArgs=['r'])
      self.accept(ConfigVariableString('key-cam-right').getValue()+'-up',self.keys_down.remove,extraArgs=['r'])
      self.accept(ConfigVariableString('key-cam-up').getValue(),self.keys_down.append,extraArgs=['u'])
      self.accept(ConfigVariableString('key-cam-up').getValue()+'-up',self.keys_down.remove,extraArgs=['u'])
      self.accept(ConfigVariableString('key-cam-left').getValue(),self.keys_down.append,extraArgs=['l'])
      self.accept(ConfigVariableString('key-cam-left').getValue()+'-up',self.keys_down.remove,extraArgs=['l'])
      self.accept(ConfigVariableString('key-cam-down').getValue(),self.keys_down.append,extraArgs=['d'])
      self.accept(ConfigVariableString('key-cam-down').getValue()+'-up',self.keys_down.remove,extraArgs=['d'])
      self.accept('mouse1-up',self.mouse_up,extraArgs=['left'])
      self.accept('mouse2-up',self.mouse_up,extraArgs=['middle'])
      

   def update(self):
      dx,dy=0,0
      if len(self.keys_down):
         out(str(self.keys_down))
      for k in self.keys_down:
         if k=='r':dx+=GamingCam.move_speed
         if k=='l':dx-=GamingCam.move_speed
         if k=='u':dy+=GamingCam.move_speed
         if k=='d':dy-=GamingCam.move_speed
         if k=='m':
            pass
            #dx+=mouse.getMouseX()
            #dy+=mouse.getMouseY()
      if self.move_enabled:
         self.move(dx,dy)

   def update_cam(self):
      self.p3dcam.setPos(   self._target,
                     0,
                     -(GamingCam.ymin+GamingCam.yshift+self._level*GamingCam.ymax),
                     GamingCam.zmin+GamingCam.zshift+self._level*GamingCam.zmax
                     )
      self.p3dcam.lookAt(self._target)

   def zoom(self,delta):
      #TODO: smoothen the zoom with a task (interpolation)
      if 0<self._level+delta<1.:
         self.level+=delta

   level=property(get_level,set_level)
   target=property(get_target,set_target)
