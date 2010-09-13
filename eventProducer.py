# -*- coding: utf-8 -*-

class eventProducer(object):
   def __init__(self):
      self.events={}
      
   def add_event(self,name):
      '''
      sets up a new event for the object.
      '''
      self.events.setdefault(name,[])
   
   def remove_event(self,name,trigger=False):
      '''
      removes an event from the list, keeping it from being triggered again.
      if trigger is set to True and callbacks have been registered,
      they are called before the event is deleted.
      '''
      if not name in self.events:
         print('WARNING: unknown event \'%s\', can\'t remove it !'%(str(name)))
      if trigger:
         self.trigger_event(name)
      del self.events[name]
   
   @property
   def event_list(self):
      '''
      returns a list of registerable events
      '''
      return self.events.keys()

   def register_event(self,name,f):
      '''
      registers a function to be called
      '''
      if not name in self.events:
         print('WARNING: unknown event \'%s\' ! registering anyway...'%(str(name)))
      self.events[name].append(f)

   def trigger_event(self,name,*args,**kwargs):
      [f(*args,**kwargs) for f in self.events[name]]
