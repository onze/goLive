#/usr/bin/make
SRC=data
SRC_GUI=$(SRC)/gui
SRC_MOD=$(SRC)/models
all: gui models

gui: main_menu game_setup gmenu

main_menu:$(SRC_GUI)/main_menu.play_btn.png $(SRC_GUI)/main_menu.load_btn.png $(SRC_GUI)/main_menu.options_btn.png $(SRC_GUI)/main_menu.quit_btn.png
	egg-texture-cards -o $(SRC_GUI)/main_menu.egg -p 176,66 $(SRC_GUI)/main_menu.play_btn.png $(SRC_GUI)/main_menu.load_btn.png $(SRC_GUI)/main_menu.options_btn.png $(SRC_GUI)/main_menu.quit_btn.png

game_setup:$(SRC_GUI)/game_setup.start_btn.png
	egg-texture-cards -o $(SRC_GUI)/game_setup.egg -p 176,66 $(SRC_GUI)/game_setup.start_btn.png

gmenu:gmenu_unit_types gmenu_units gmenu_launch_btn unit_conf

gmenu_unit_types:$(SRC_GUI)/gmenu/type.builders.png $(SRC_GUI)/gmenu/type.markers.png $(SRC_GUI)/gmenu/type.fighters.png
	egg-texture-cards -o $(SRC_GUI)/gmenu/unit_types_btn.egg -p 100,100 $(SRC_GUI)/gmenu/type.builders.png $(SRC_GUI)/gmenu/type.markers.png $(SRC_GUI)/gmenu/type.fighters.png

gmenu_units:$(SRC_GUI)/gmenu/h_sprinter.png $(SRC_GUI)/gmenu/v_sprinter.png $(SRC_GUI)/gmenu/zigzagger.png $(SRC_GUI)/gmenu/cw-spiraler.png $(SRC_GUI)/gmenu/ccw-spiraler.png $(SRC_GUI)/gmenu/circler.png $(SRC_GUI)/gmenu/guard.png $(SRC_GUI)/gmenu/archer.png $(SRC_GUI)/gmenu/assassin.png
	egg-texture-cards -o $(SRC_GUI)/gmenu/units_btn.egg -p 100,100 $(SRC_GUI)/gmenu/h_sprinter.png $(SRC_GUI)/gmenu/v_sprinter.png $(SRC_GUI)/gmenu/zigzagger.png $(SRC_GUI)/gmenu/cw-spiraler.png $(SRC_GUI)/gmenu/ccw-spiraler.png $(SRC_GUI)/gmenu/circler.png $(SRC_GUI)/gmenu/guard.png $(SRC_GUI)/gmenu/archer.png $(SRC_GUI)/gmenu/assassin.png

unit_conf:$(SRC_GUI)/gmenu/v_arrow.png $(SRC_GUI)/gmenu/h_arrow.png $(SRC_GUI)/gmenu/tile-picking.png $(SRC_GUI)/gmenu/wall-picking.png $(SRC_GUI)/gmenu/unit-picking.png
	egg-texture-cards -o $(SRC_GUI)/gmenu/unit_conf.egg -p 100,100 $(SRC_GUI)/gmenu/v_arrow.png $(SRC_GUI)/gmenu/h_arrow.png $(SRC_GUI)/gmenu/tile-picking.png $(SRC_GUI)/gmenu/wall-picking.png $(SRC_GUI)/gmenu/unit-picking.png
	
gmenu_launch_btn:$(SRC_GUI)/gmenu/launch_btn.png
	egg-texture-cards -o $(SRC_GUI)/gmenu/launch_btn.egg -p 200,100 $(SRC_GUI)/gmenu/launch_btn.png

models:
	#"skipping models cause blender/chicken console exports sucks a bit =/"
	#export chicken_sel=tile
	#blender -b $(SRC_MOD)/tile.blend -P ~/.blender/scripts/chicken_exportR85.py

clean:
	rm -rf *.pyc
	rm -rf *.pyo
	rm -f $(SRC_GUI)/main_menu.egg
	rm -f $(SRC_GUI)/game_setup.egg
	rm -f $(SRC_GUI)/gmenu.units_btn.egg
	rm -f $(SRC_GUI)/gmenu.launch_btn.egg
