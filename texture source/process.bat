REM to_tiles takes the following arguments: [output folder] [spritesheet] [type] [bordering] [transition] [tile width] [tile height]
REM This doesn't generate every single tile, but it surely speeds up things

"../tools/to_tiles.py" "%~dp0\../textures/terrain/tiles/" "sea_river.png" 3 3,4 1 16 16
"../tools/to_tiles.py" "%~dp0\../textures/terrain/tiles/" "road_plains.png" 5 4,5 0,1,2,3 16 16
"../tools/to_tiles.py" "%~dp0\../textures/terrain/tiles/" "river_plains.png" 1 1,4 0,2,5 16 16
"../tools/to_tiles.py" "%~dp0\../textures/terrain/tiles/" "bridge_river.png" 4 1,4,5 1 16 16
"../tools/to_tiles.py" "%~dp0\../textures/terrain/tiles/" "bridge_sea.png" 4 1,4,5 3 16 16

PAUSE