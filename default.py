
from panda3d.core import ConfigVariableBool,ConfigVariableInt,ConfigVariableString
'''
ConfigVariableString('','')
ConfigVariableInt('',)
'''
ConfigVariableInt('load-propagation-frequency',10)
ConfigVariableInt('load-level-0',5)
ConfigVariableInt('load-level-1',50)
ConfigVariableInt('load-level-2',255)
ConfigVariableInt('pawner-duration',20)
ConfigVariableInt('win-width',1280)
ConfigVariableInt('win-height',800)
ConfigVariableString('console-trigger','`')
ConfigVariableString('key-confirm','enter')
ConfigVariableInt('intro-delay',1)
ConfigVariableBool('dev-mode','t')
ConfigVariableString('key-cam-zoom-in','wheel_up')
ConfigVariableString('key-cam-zoom-out','wheel_down')
ConfigVariableString('key-cam-right','arrow_right')
ConfigVariableString('key-cam-up','arrow_left')
ConfigVariableString('key-cam-left','arrow_up')
ConfigVariableString('key-cam-down','arrow_down')
ConfigVariableInt('map-width-xs',8)
ConfigVariableInt('map-height-xs',8)

#default values for game configuration
game_conf={'cpu':True,
		   'map.res':'xs',
		   }
