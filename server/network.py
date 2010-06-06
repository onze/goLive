'''
this file list constants that represent nature of data sent between client and server.
typically, cts==client to server, stc==server to client
some global vars are also set from different modules:
-serverproxy: set in serverproxy.py
'''
serverproxy=None

#import cPickle
import sys



def inf():
	'''return a new number each call'''
	for i in xrange(sys.maxint):
		yield i
	raise Exception('maxint reached.')
next=inf().next

def dict2packet(d):
	#TODO: test compression here
	return str(d)+'\n'
#	return cPickle.dumps(d,cPickle.HIGHEST_PROTOCOL)+'\n'

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
stc_tile_sync=next()
#build home:{meta:{pid:1/2,pos:(42,42)}}
stc_newhome=next()
#build unit:{meta:{unit_type:type,pid:1/2,eid:number,x:number,y:number}}
stc_new_unit=next()
#current unit starts a move toward a tile:{meta:{
#eid:unit eid number,
#start:tile eid number at beginning of move,
#end:tile eid number at end of move,
#begin:frame number of when the move starts
#frames: number of frames dedicated to the move
#}}
stc_unit_moving=next()
#unit has reached its target:{meta:{eid:unit's eid,tile:target's eid}}
stc_unit_move_over=next()
#no need yet for this one
#unit has moved to a new tile. inform client:{meta:{eid:unit eid,tile:tile's eid}}
#stc_unit_tile=next()

