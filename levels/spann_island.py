#================================================================================
# Level info
level.name = 'Spann Island'
level.author = 'Advance Wars 2'
level.description = 'Taken from Advance Wars 2, Versus, War Room'

level.supportedDatabases = ['AI Wars']
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
player1 = level.getPlayerData(0)
player1.addBuilding(level.getBuildingAtPosition(Point(1, 5)))
player1.addBuilding(level.getBuildingAtPosition(Point(1, 6)))
player1.addBuilding(level.getBuildingAtPosition(Point(2, 6)))
player1.addBuilding(level.getBuildingAtPosition(Point(2, 7)))
player1.addBuilding(level.getBuildingAtPosition(Point(3, 7)))

player2 = level.getPlayerData(1)
player2.addBuilding(level.getBuildingAtPosition(Point(11, 1)))
player2.addBuilding(level.getBuildingAtPosition(Point(13, 1)))
player2.addBuilding(level.getBuildingAtPosition(Point(12, 2)))
player2.addBuilding(level.getBuildingAtPosition(Point(13, 2)))
player2.addBuilding(level.getBuildingAtPosition(Point(13, 3)))
