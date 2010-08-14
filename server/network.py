
'''
this file list constants that represent nature of data sent between client and server.
cts==client to server, stc==server to client
some global vars are also set from different modules:
-serverproxy: set in serverproxy.py
'''

serverproxy=None

import atexit
#import cPickle
import sys

from panda3d.core import ConfigVariableBool

import node

def inf():
	'''return a new number each call'''
	for i in xrange(sys.maxint):
		yield i
	raise Exception('maxint reached.')

'''each attribute set to next() will have a unique value within the module.'''
next=inf().next

'''packet secondary meta. indicates whether or not the data contained in the packet is buffered.'''
buffered_data_flag=next()

def dict2packet(d,buffered=False):
	'''
	takes a dict and returns a string packet ready to be sent through the wires.
	packet is added a meta indicating whether or not it contains buffered data. this meta handling is transparent for the game logic,
	since it is added after the call to Node.send, and removed before the yielding in the call to Node.read.
	'''
	#TODO: test compression here
	d[buffered_data_flag]=int(buffered)
	return str(d)+'\n'
#	return cPickle.dumps(d,cPickle.HIGHEST_PROTOCOL)+'\n'

def buffer2packets(buf):
	'''
	maximizes packet dataload usage by breaking the given buffer's packets in packets respecting Node.MTU.
	for example:
	from  buf=
	{
	'meta0':[{'dat':'short'},{'dat': 'average'},{'dat':'looooooooooooooooooooooooooooooooooooooooooooooooooong'},],
	'meta1':[{'dat':'looooooooooooooooooooooooooooooooooooooooooooooooooong'},{'dat':'short'},]
	}
	----------------------------------------------------------------------------------|<-MTU
	to packets=
	[
	{'meta0':[{'dat':'short'},{'dat': 'average'}]},
	{'meta0':[{'dat':'looooooooooooooooooooooooooooooooooooooooooooooooooong'}]},
	{'meta1':[{'dat':'looooooooooooooooooooooooooooooooooooooooooooooooooong'}]},
	{'meta1':[{'dat':'short'}]},
	]
	returned packets are single meta-ed, to keep a network/cpu efficiency balance.
	'''
	packets=[]
	while len(buf):
		meta,data=buf.popitem()
		currpkt={meta:[]}
		currpktlen=len(dict2packet(currpkt,buffered=True))
		#Node.bufferize has made sure data is not empty
		fragment=data.pop(0)
		while len(data):
			#packet would be too big, save it and create new one.
			#the +3 comes from the comma+space+\n that are appended to the fragment during packet creation
			#this breaks dict2packet's encapsulation for less worse efficiency
			if currpktlen+len(str(fragment))+3>=node.Node.MTU:
				packets.append(dict2packet(currpkt,buffered=True))
				#print 'built packet:',dict2packet(currpkt,buffered=True)
				currpkt={meta:[]}
				currpktlen=len(dict2packet(currpkt,buffered=True))
				#make sure base packet can be sent
				assert currpktlen<node.Node.MTU,'ERROR in buffer2packets: \
				empty packet is already too big (packet length=%i,Node.MTU=%i). \
				check meta length.\nmeta=%s\n packet=%s\
				'%(currpktlen,node.Node.MTU,meta,dict2packet(currpkt))
			else:
				currpkt[meta].append(fragment)
				currpktlen=len(dict2packet(currpkt,buffered=True))
				fragment=data.pop(0)
		currpkt[meta].append(fragment)
		#print 'built last packet for current meta:',dict2packet(currpkt,buffered=True)
		packets.append(dict2packet(currpkt,buffered=True))
	return packets

def packet2dict(p):
	#TODO: test decompression here
	return eval(p)
#	return cPickle.loads(p)

network_non_buffered_packets=[]
network_buffered_packets=[]

if ConfigVariableBool('dump-network-packets').getValue():	
	def code2meta(code):
		d=globals()
		for k in d:
			if (k.startswith('stc_') or k.startswith('cts_')) and d[k]==code:
				return k
		return None

	def print_packet_detail(pkt):
		if len(pkt):
			meta,data=pkt.popitem()
			meta='%s (%s)'%(meta,code2meta(meta))
			print {meta:data}
			return 0
		return 1
	
	def dump_network_packets():
		mask=[stc_new_tile]
		print '===network packets dumping==='
		print 'masked metas:',mask
		def dump_buffer(buf):
			avglen=[]
			masked_packets=0
			for pkt in buf:
				avglen.append(len(pkt))
				pkt=packet2dict(pkt)
				del pkt[buffered_data_flag]
				for m in mask:
					if pkt.has_key(m):
						del pkt[m]
				masked_packets+=print_packet_detail(pkt)
			print 'masked packets:',masked_packets
			if len(avglen):
				avglen.sort()
				print 'lengths min/max:',avglen[0],'/',avglen[-1],', average:',str(sum(avglen)/float(len(avglen))),' MTU:',node.Node.MTU
		print '==non buffered packets (%i)=='%(len(network_non_buffered_packets))
		dump_buffer(network_non_buffered_packets)
		print '==buffered packets (%i)=='%(len(network_buffered_packets))
		dump_buffer(network_buffered_packets)
		print '\nnetwork dumping done.'
	atexit.register(dump_network_packets)
	
####################
# CLIENT TO SERVER #
####################
###<debug metas>
#asks for a print
#meta:{eid:number}
cts_dbg_dump_entity=next()

###</debug metas>
#the newly created game's requested configuration
#gmap.res:s/m/l for small/medium/large, map resolution
#cpu: boolean, played against an AI or against a player
cts_conf=next()

#launch new unit. confs are:
#{'unit_type':'v_sprinter','x':number, 'y':number }
#{'unit_type':'h_sprinter','x':number, 'y':number }
cts_new_unit=next()

####################
# SERVER TO CLIENT #
####################
#GENERAL CONTROL

#server configuration
stc_conf=next()

#each newly created player send its pid to its client
#{network.pid_setup:{'pid':self.pid}}
stc_pid_setup=next()

#server says the game is over
stc_end_game=next()

#server says the game starts
stc_start_game=next()

#sync tile eid,x,y with clients ones:{meta:{eid:number,x:number,y:number}}
stc_new_tile=next()

#a unit drops a pawn on a tile: {meta:{eid:tile eid,pawner: player pid}}
stc_tile_change_pawner=next()

#build home:{meta:{pid:1/2,pos:(42,42)}}
stc_new_home=next()

#build unit:{meta:{unit_type:type,pid:1/2,eid:number,x:number,y:number}}
stc_new_unit=next()

#path transmission:{meta:{
#eid:unit eid number
#path:list of tile to pass by
#}}
stc_unit_add_path=next()

#unit has finished moving and needs to be removed
#eid: unit eid
#tile: tile eid
stc_unit_move_over=next()

#tile ratio has changed
#ratio: dict {pid:ratio}
stc_tile_ratio_change=next()



