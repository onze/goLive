
import socket

import server.network 

class Node:
   MTU=1024
   def __init__(self,socket):
      self.socket=socket
      self.string_buffer=''
      self.dict_buffer={}
      
   def bufferize(self,d):
      '''
      transforming
      {metaM:{var1:x,var2:y}}
      +{metaM:{var3:s,var4:t}}
      +{metaN:{var5:u,var6:v}}
      into
      {metaM:{var1:x,var2:y,var3:s,var4:t},
      metaN:{var5:u,var6:v}}
      '''
      [self.dict_buffer.setdefault(meta,{}).update(d[meta]) for meta in d]

   def flush_buffer(self):
      '''
      flush buffered data
      '''
      [self.send_string(pkt) for pkt in server.network.dict2packets(self.dict_buffer)]
      self.dict_buffer={}
      
   def read(self):
      try:
         self.buf+=self.socket.recv(4096)
      except socket.error,msg:
         print 'unable to read serverproxy\'s socket: ('+str(msg)+')'
      while '\n' in self.buf:
         i=self.buf.index('\n')
         try:
            yield server.network.packet2dict(self.buf[:i])
         except Exception,e:
            print 'serverproxy error:',str(e)
         self.buf=self.buf[i+1:]

   def send(self,d):
      '''
      sends the packet, fragmenting it as MTU sized packets if needed
      '''
      self.socket.send(server.network.dict2packet(d))

   def send_string(self,s):
      '''
      sends the string as is.
      '''
      self.socket.send(s)