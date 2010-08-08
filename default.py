
from panda3d.core import ConfigVariableBool,ConfigVariableInt,ConfigVariableString
'''
ConfigVariableString('','')
ConfigVariableInt('',)
'''
def load_panda_default():
	#dev
	ConfigVariableBool('dev-mode',True)
	ConfigVariableBool('stats',False)
	ConfigVariableBool('dump-network-packets',True)
	
	#engine
	ConfigVariableInt('win-width',1280)
	ConfigVariableInt('win-height',800)
	ConfigVariableInt('intro-delay',1)
	
	#keys	
	ConfigVariableString('console-trigger','`')
	ConfigVariableString('key-confirm','enter')
	ConfigVariableString('gmenu-cancel','q')
	ConfigVariableString('gmenu-m1','w')
	ConfigVariableString('gmenu-m2','e')
	ConfigVariableString('gmenu-m3','r')
	ConfigVariableString('gmenu-launch','space')
	ConfigVariableString('key-cam-zoom-in','wheel_up')
	ConfigVariableString('key-cam-zoom-out','wheel_down')
	ConfigVariableString('key-cam-right','arrow_right')
	ConfigVariableString('key-cam-up','arrow_left')
	ConfigVariableString('key-cam-left','arrow_up')
	ConfigVariableString('key-cam-down','arrow_down')
	
	#game
	ConfigVariableInt('map-width-xs',8)
	ConfigVariableInt('map-height-xs',8)
	ConfigVariableInt('map-width-s',16)
	ConfigVariableInt('map-height-s',16)
	ConfigVariableInt('map-width-m',32)
	ConfigVariableInt('map-height-m',32)
	ConfigVariableInt('map-width-l',48)
	ConfigVariableInt('map-height-l',48)
	ConfigVariableInt('map-width-xl',64)
	ConfigVariableInt('map-height-xl',64)

#default values for game configuration
game_conf={'cpu':True,
		   'map.res':'m',
		   }
