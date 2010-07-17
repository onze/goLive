###########################################################
###                                                     ###
### Panda3D Configuration File -  User-Editable Portion ###
###                                                     ###
###########################################################

# Uncomment one of the following lines to choose whether you should
# run using OpenGL, DirectX or TinyPanda (software) rendering.
# There can only be one load-display line, but you can use
# multiple aux-display lines to specify fallback modules.
# When the module indicated by load-display fails, it will fall
# back to the next display module indicated by aux-display,
# when that fails, the next aux-display line, and so on.

load-display pandagl
#load-display pandadx9
#load-display pandadx8
#load-display tinydisplay

# These control the placement and size of the default rendering window.

win-origin 0 0
win-size 1280 800
win-width 1280
win-height 800

# Uncomment this line if you want to run Panda fullscreen instead of
# in a window.

fullscreen t

# The framebuffer-hardware flag forces it to use an accelerated driver.
# The framebuffer-software flag forces it to use a software renderer.
# If you don't set either, it will use whatever's available.

framebuffer-hardware #t
framebuffer-software #f

# These set the minimum requirements for the framebuffer.
# A value of 1 means: get as many bits as possible,
# consistent with the other framebuffer requirements.

depth-bits 1
color-bits 1
alpha-bits 0
stencil-bits 0
multisamples 0

# These control the amount of output Panda gives for some various
# categories.  The severity levels, in order, are "spam", "debug",
# "info", "warning", and "error"; the default is "info".  Uncomment
# one (or define a new one for the particular category you wish to
# change) to control this output.

notify-level warning
default-directnotify-level warning

# These specify where model files may be loaded from.  You probably
# want to set this to a sensible path for yourself.  $THIS_PRC_DIR is
# a special variable that indicates the same directory as this
# particular Config.prc file.

model-path    $MAIN_DIR
model-path    /usr/share/panda3d
model-path    /usr/share/panda3d/models

# This enable the automatic creation of a TK window when running
# Direct.

want-directtools  #f
want-tk           #f

# Enable/disable performance profiling tool and frame-rate meter

want-pstats            #f
show-frame-rate-meter  t

# Enable audio using the FMOD audio library by default:

audio-library-name p3openal_audio

# Enable the use of the new movietexture class.

use-movietexture #t

# The new version of panda supports hardware vertex animation, but it's not quite ready

hardware-animated-vertices #f

# Enable the model-cache, but only for models, not textures.

model-cache-dir $USER_APPDATA/.panda3d/cache
model-cache-textures #f

# This option specifies the default profiles for Cg shaders.
# Setting it to #t makes them arbvp1 and arbfp1, since these
# seem to be most reliable. Setting it to #f makes Panda use
# the latest profile available.
# This default profile can be overriden by any profile setting
# from within the application.

clock-mode limited 
clock-frame-rate 60

basic-shaders-only #t
direct-gui-edit f
audio-library-name null

#notify-level spam
#default-directnotify-level info

want-pstat 1
task-timer-verbose 1
pstats-tasks 1
#############################################################golive custom settings
###development variables
console-trigger `
dev-mode t

###client settings
#general settings
intro-delay 1

#key handling
key-confirm enter
key-next space
key-cancel escape

#camera movement while gaming
key-cam-zoom-in wheel_up
key-cam-zoom-out wheel_down
key-cam-right arrow_right
key-cam-left arrow_left
key-cam-up arrow_up
key-cam-down arrow_down

#unit setup menu
#TODO setup qwert/azerty layout handling here

###server settings
#map resolution for each size
map-width-xs 8
map-height-xs 8
map-width-s 16
map-height-s 16
map-width-m 32
map-height-m 32
map-width-l 64
map-height-l 64

#tiles owner propagation
pawner-duration 20
load-propagation-frequency 10
load-level-level-0 5
load-level-level-1 50
load-level-level-2 255


