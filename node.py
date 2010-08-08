from panda3d.core import ConfigVariableBool

import errno
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
      '''
#      print 'Node.bufferize()',d
      for meta in d:
         data=d[meta]
         if len(data):
            self.dict_buffer.setdefault(meta,[]).append(data)
#      print 'buffer=',self.dict_buffer

   def flush_buffer(self):
      '''
      flush buffered data packets.
      '''
      if len(self.dict_buffer)==0:
         return
      packets=server.network.buffer2packets(self.dict_buffer)
      for s in packets:
         if ConfigVariableBool('dump-network-packets').getValue():
            server.network.network_buffered_packets.append(s)
         self.send_string(s)
      self.dict_buffer={}
      
   def read(self):
      '''
      yields message received from socket.
      '''
      try:
         self.buf+=self.socket.recv(4096)
      except socket.error:
         #nothing to read, so nothing to do
         return
         #print 'unable to read serverproxy\'s socket: ('+str(msg)+')'
      while '\n' in self.buf:
         i=self.buf.index('\n')
         try:
            packet=server.network.packet2dict(self.buf[:i])
         except Exception,e:
            print 'serverproxy error:',str(e)
         #develop buffered data into multiple packets
         buffered=bool(packet[server.network.buffered_data_flag])
         del packet[server.network.buffered_data_flag]
         if buffered==True:
            for meta in packet:
               for data in packet[meta]:
                  yield {meta:data}
         else:
            yield packet
         self.buf=self.buf[i+1:]

   def send(self,d):
      '''
      make a apcket out of the given dicts and sends it as a string.
      '''
      s=server.network.dict2packet(d)
      if ConfigVariableBool('dump-network-packets').getValue():
         server.network.network_non_buffered_packets.append(s)
      self.send_string(s)

   def send_string(self,s):
      '''
      sends the string as is.
      this method is the only one that actually uses the socket.
      '''
      self.socket.send(s)