
from direct.gui.DirectGui import DirectButton,OnscreenText

from widgetwrapper import Button,Frame,Spacer
import layout

class Main_menu(Frame):
   sgn_play='Main_menu.sgn_play'
   sgn_load='Main_menu.sgn_load'
   sgn_options='Main_menu.sgn_options'
   sgn_quit='Main_menu.sgn_quit'

   def __init__(self,*args,**kwargs):
      kwargs['layout']=layout.HLayout
      Frame.__init__(self,*args,**kwargs)
      res=loader.loadModel('data/gui/main_menu.egg')
      self.resources = {   'play_btn':res.find('**/main_menu.play_btn'),
                     'load_btn':res.find('**/main_menu.load_btn'),
                     'options_btn':res.find('**/main_menu.options_btn'),
                     'quit_btn':res.find('**/main_menu.quit_btn')
                     }

   def open(self):
      #left spacer
      Spacer(parent=self)

      self.middle_frame=Frame(layout=layout.VLayout,
                        parent=self,
                         pref_w=180)
      n=5
      [Spacer(parent=self.middle_frame) for _ in range(n)]
      self.quit_btn=Button(   pref_h=70,
                        p3dobject=DirectButton(geom=(self.resources['quit_btn']),
                                          borderWidth=(0,0),
                                          command=messenger.send, extraArgs=[Main_menu.sgn_quit]),
                        parent=self.middle_frame)
      Spacer(parent=self.middle_frame)
      self.options_btn=Button(pref_h=70,
                        p3dobject=DirectButton(geom=(self.resources['options_btn']),
                                          borderWidth=(0,0),
                                          command=messenger.send, extraArgs=[Main_menu.sgn_options]),
                        parent=self.middle_frame)
      self.load_btn=Button(   pref_h=70,
                        p3dobject=DirectButton(geom=(self.resources['load_btn']),
                                          borderWidth=(0,0),
                                          command=messenger.send, extraArgs=[Main_menu.sgn_load]),
                        parent=self.middle_frame)
      self.play_btn=Button(   pref_h=70,
                        p3dobject=DirectButton(geom=(self.resources['play_btn']),
                                          borderWidth=(0,0),
                                          command=messenger.send, extraArgs=[Main_menu.sgn_play]),
                        parent=self.middle_frame)
      [Spacer(parent=self.middle_frame) for _ in range(n)]
      
      #right spacer
      Spacer(parent=self)
      
      self.message=OnscreenText(text='main menu',style=1,fg=(1,1,1,1),pos=(.87,-.95),scale=.07)

   def close(self):
      self.play_btn.p3dobject.destroy()
      del self.play_btn
      self.load_btn.p3dobject.destroy()
      del self.load_btn
      self.options_btn.p3dobject.destroy()
      del self.options_btn
      self.quit_btn.p3dobject.destroy()
      del self.quit_btn
      del self.middle_frame
      self.message.destroy()
      del self.message

