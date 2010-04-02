#================================================================================
# Level info
level.name = 'Spann Island'
level.playerCount = 2

#================================================================================
# Terrain data
level.setTileData( [[7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
                    [7,  7,  1,  2,  0,  0,  5,  0,  0,  1,  2,  10, 1,  10, 7],
                    [7,  1,  1,  2,  0,  2,  7,  1,  0,  9,  1,  1,  11, 10, 7],
                    [7,  9,  9,  0,  0,  7,  7,  7,  0,  1,  3,  1,  0,  10, 7],
                    [7,  1,  1,  0,  1,  7,  7,  7,  0,  9,  3,  9,  0,  1,  7],
                    [7,  10, 0,  0,  9,  7,  7,  2,  0,  0,  0,  0,  0,  9,  7],
                    [7,  10, 11, 1,  1,  1,  1,  2,  2,  1,  7,  7,  5,  7,  7],
                    [7,  7,  10, 10, 1,  1,  1,  1,  1,  1,  7,  7,  1,  1,  7],
                    [7,  7,  7,  7,  3,  9,  3,  2,  9,  1,  5,  1,  9,  9,  7],
                    [7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7]] )

#================================================================================
# Player starting buildings
player1 = level.addPlayer()
player1.addBuilding(level.getBuildingAt(1, 5))
player1.addBuilding(level.getBuildingAt(1, 6))
player1.addBuilding(level.getBuildingAt(2, 6))
player1.addBuilding(level.getBuildingAt(2, 7))
player1.addBuilding(level.getBuildingAt(3, 7))

player2 = level.addPlayer()
player2.addBuilding(level.getBuildingAt(11, 1))
player2.addBuilding(level.getBuildingAt(13, 1))
player2.addBuilding(level.getBuildingAt(12, 2))
player2.addBuilding(level.getBuildingAt(13, 2))
player2.addBuilding(level.getBuildingAt(13, 3))
