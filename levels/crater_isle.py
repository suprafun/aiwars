#================================================================================
# Level info
level.name = 'Crater Isle'
level.author = 'Advance Wars 2'
level.description = 'Taken from Advance Wars 2, Versus, Classic'

level.supportedDatabases = ['AI Wars']
level.playerCount = 2

#================================================================================
# Terrain data
level.setTileData( [[7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
                    [7,  7,  7,  7,  7,  7,  1,  1,  1,  1,  1,  1,  7,  7,  7,  7],
                    [7,  7,  7,  7,  10, 11, 10, 0,  9,  9,  9,  9,  1,  1,  7,  7],
                    [7,  7,  1,  1,  0,  10, 1,  1,  1,  1,  1,  2,  2,  2,  2,  7],
                    [7,  1,  9,  10, 0,  1,  1,  1,  9,  9,  2,  2,  2,  2,  1,  7],
                    [7,  1,  1,  0,  0,  9,  1,  7,  1,  2,  2,  2,  2,  2,  9,  7],
                    [7,  1,  1,  0,  1,  1,  7,  7,  1,  7,  7,  1,  2,  2,  2,  7],
                    [7,  3,  1,  0,  3,  7,  7,  7,  7,  7,  7,  9,  2,  2,  1,  7],
                    [7,  1,  0,  0,  1,  7,  7,  7,  7,  7,  7,  2,  2,  2,  9,  7],
                    [7,  9,  0,  1,  9,  7,  7,  1,  1,  7,  1,  2,  2,  2,  2,  7],
                    [7,  1,  0,  3,  1,  1,  1,  9,  1,  1,  1,  1,  1,  1,  1,  7],
                    [7,  9,  0,  0,  0,  3,  1,  1,  9,  1,  1,  10, 1,  10, 9,  7],
                    [7,  7,  1,  1,  0,  0,  0,  1,  1,  10, 1,  10, 1,  1,  7,  7],
                    [7,  7,  7,  9,  1,  1,  0,  0,  9,  1,  10, 11, 10, 7,  7,  7],
                    [7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7]] )

#================================================================================
# Player starting level.getBuildingAtPosition(Point(Point(
player1 = level.addPlayer()
player1.addBuilding(level.getBuildingAtPosition(Point(5, 3)))
player1.addBuilding(level.getBuildingAtPosition(Point(6, 3)))
player1.addBuilding(level.getBuildingAtPosition(Point(7, 3)))
player1.addBuilding(level.getBuildingAtPosition(Point(9, 3)))
player1.addBuilding(level.getBuildingAtPosition(Point(10, 3)))
player1.addBuilding(level.getBuildingAtPosition(Point(11, 3)))
player1.addBuilding(level.getBuildingAtPosition(Point(6, 4)))
player1.addBuilding(level.getBuildingAtPosition(Point(3, 5)))
player1.addBuilding(level.getBuildingAtPosition(Point(4, 5)))
player1.addBuilding(level.getBuildingAtPosition(Point(9, 5)))
player1.addBuilding(level.getBuildingAtPosition(Point(6, 6)))

player2 = level.addPlayer()
player2.addBuilding(level.getBuildingAtPosition(Point(11, 12)))
player2.addBuilding(level.getBuildingAtPosition(Point(10, 13)))
player2.addBuilding(level.getBuildingAtPosition(Point(11, 13)))
player2.addBuilding(level.getBuildingAtPosition(Point(12, 13)))
