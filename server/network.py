'''
this file list constants that represent nature of data sent between client and server.
cts==client to server, stc==server to client
some global vars are also set from different modules:
-serverproxy: set in serverproxy.py
'''
serverproxy=None

#import cPickle
import sys

import node

def inf():
	'''return a new number each call'''
	for i in xrange(sys.maxint):
		yield i
	raise Exception('maxint reached.')
next=inf().next

def dict2packet(d):
	'''
	takes a dict and returns a string packet ready to be sent through the wires
	'''
	#TODO: test compression here
	return str(d)+'\n'
#	return cPickle.dumps(d,cPickle.HIGHEST_PROTOCOL)+'\n'

def dict2packets(dbuf):
	'''
	takes a dict buffer and returns a list of string packets ready to be sent through the wires.
	strings size doesn't exceed Node.MTU (upd networking to come soon..)
	'''
	#TODO: test zlib compression here
#	print 'dict2packets',dbuf,'\n with MTU=',node.Node.MTU
	packets=[]
	while len(dbuf):
		meta,data=dbuf.popitem()
		pkt=dict2packet({meta:data})
		if len(pkt)<node.Node.MTU:
			#print 'built packet directly',pkt,'packet length:',len(pkt)
			packets.append(pkt)
		else:
			#print 'fragmenting',pkt
			fragment={meta:{}}
			s=dict2packet(fragment)
			assert len(s)<=node.Node.MTU,'fragment base (\''+s+'\') has lenght '+str(len(s))+' while MTU='+str(node.Node.MTU)
			while len(data):
				nextitem=data.popitem()
				fragment[meta].update((nextitem,))
				if len(dict2packet(fragment))>node.Node.MTU:
					if len(fragment[meta])==1:
						out('ERROR: in network.dict2packets: fragment will never be able to get this item within MTU limits.\
						item=%s, MTU=%i. skipping item.'%(dict2packet(fragment),node.Node.MTU))
						continue
					data.update((nextitem,))
					del fragment[meta][nextitem[0]]
					packets.append(dict2packet(fragment))
					#print 'built packet fragment',fragment
					fragment={meta:{}}
			packets.append(dict2packet(fragment))
	return packets

def packet2dict(p):
	#TODO: test decompression here
	return eval(p)
#	return cPickle.loads(p)

####################
# CLIENT TO SERVER #
####################
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

#server says the game is over
stc_end_game=next()

#server says the game starts
stc_start_game=next()

#sync tile eid,x,y with clients ones:{meta:{eid:number,x:number,y:number}}
stc_new_tile=next()

#a unit drops a pawn on a tile: {meta:{eid:tile eid,pawner: player pid}}
stc_tile_change_pawner=next()

#tile load_level update {meta:{
#eid:tile eid number
#owner: owner pid
#level: tile load_level
#}}
#TODO: buffer this into {meta:[{eid:load_level},{eid:load_level},...]}!
stc_tile_load_level_change=next()

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





