
from quadtree import QuadTree

class GTileQuadTree(QuadTree):
   '''
   subclasses a generic quad tree, taking GTiles as leaves and PandaNodes as nodes.
   '''
   def __init__(self,resx,resy):
      QuadTree.__init__(self,resx/2,resy/2,resx,resy)
      self.p3dobject=self.map.root.attachNewNode('quadtree_p3droot')
      self.register_event('new_node',self.on_new_node)
      self.register_event('new_leaf',self.on_new_leaf)
   
   def on_new_node(self,node,parent,old_leaf):
      node.p3dobject=parent.p3dobject.attachNewNode('quadtree_node_%i_%i'%(node.x,node.y))
      old_leaf.data.p3dobject.wrtReparentTo(node.p3dobject)
      node.register_event('new_node',self.on_new_node)
      node.register_event('new_leaf',self.on_new_leaf)

   def on_new_leaf(self,leaf,parent_node):
      leaf.data.p3dobject.wrtReparentTo(parent_node.p3dobject)