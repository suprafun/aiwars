#================================================================================
# Level info
level.name = 'Duo Falls'
level.author = 'Advance Wars 2'
level.description = 'Taken from Advance Wars 2, Versus, War Room'

level.supportedDatabases = ['AI Wars']
level.playerCount = 2

#================================================================================
# Terrain data
level.setTileData( [[7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
                    [7,  7,  7,  7,  7,  7,  7,  1,  1,  1,  1,  4,  1,  1,  1,  7,  7,  7,  7,  7,  7,  1,  1,  4,  1,  2,  1,  7,  7,  7,  7,  7,  7],
                    [7,  7,  7,  1,  1,  2,  2,  1,  9,  9,  1,  4,  1,  9,  1,  1,  7,  7,  7,  2,  2,  9,  9,  4,  1,  0,  2,  2,  1,  1,  7,  7,  7],
                    [7,  2,  2,  2,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  1,  7,  7,  7,  1,  0,  0,  0,  5,  0,  0,  1,  1,  2,  2,  1,  7,  7],
                    [7,  2,  2,  2,  0,  2,  1,  1,  1,  2,  2,  4,  1,  2,  0,  1,  7,  7,  7,  10, 0,  1,  2,  4,  1,  0,  1,  10, 1,  1,  9,  1,  7],
                    [7,  2,  2,  10, 0,  10, 1,  9,  9,  1,  1,  4,  1,  1,  0,  9,  7,  7,  7,  2,  0,  9,  7,  7,  7,  0,  10, 11, 10, 1,  2,  2,  7],
                    [7,  2,  1,  1,  11, 1,  1,  1,  1,  2,  7,  7,  7,  1,  0,  2,  7,  7,  7,  1,  0,  1,  7,  7,  7,  0,  0,  10, 1,  1,  2,  2,  7],
                    [7,  1,  1,  10, 0,  10, 1,  2,  2,  2,  7,  7,  7,  10, 0,  1,  7,  7,  7,  12, 0,  2,  7,  7,  7,  1,  12, 1,  12, 1,  2,  2,  7],
                    [7,  1,  1,  12, 0,  12, 1,  7,  7,  2,  7,  7,  7,  1,  0,  1,  1,  7,  1,  1,  0,  1,  7,  7,  7,  1,  1,  1,  1,  9,  9,  1,  7],
                    [7,  1,  9,  9,  0,  9,  9,  2,  2,  2,  7,  7,  7,  2,  0,  1,  9,  1,  9,  2,  0,  9,  7,  7,  7,  9,  9,  1,  1,  3,  1,  7,  7],
                    [7,  7,  1,  1,  1,  1,  2,  2,  2,  2,  7,  7,  7,  1,  0,  0,  0,  0,  0,  0,  0,  2,  7,  7,  7,  2,  1,  3,  3,  7,  7,  7,  7],
                    [7,  7,  7,  1,  2,  2,  2,  2,  7,  7,  7,  7,  7,  7,  1,  2,  2,  9,  2,  2,  2,  7,  7,  7,  7,  1,  7,  7,  7,  7,  7,  7,  7],
                    [7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7]] )

#================================================================================
# Player starting buildings
player1 = level.getPlayerData(0)
player1.addBuilding(level.getBuildingAtPosition(Point(3, 5)))
player1.addBuilding(level.getBuildingAtPosition(Point(5, 5)))
player1.addBuilding(level.getBuildingAtPosition(Point(4, 6)))
player1.addBuilding(level.getBuildingAtPosition(Point(3, 7)))
player1.addBuilding(level.getBuildingAtPosition(Point(5, 7)))
player1.addBuilding(level.getBuildingAtPosition(Point(3, 8)))
player1.addBuilding(level.getBuildingAtPosition(Point(5, 8)))
player1.addBuilding(level.getBuildingAtPosition(Point(2, 9)))
player1.addBuilding(level.getBuildingAtPosition(Point(3, 9)))
player1.addBuilding(level.getBuildingAtPosition(Point(5, 9)))
player1.addBuilding(level.getBuildingAtPosition(Point(6, 9)))

player2 = level.getPlayerData(1)
player2.addBuilding(level.getBuildingAtPosition(Point(21, 2)))
player2.addBuilding(level.getBuildingAtPosition(Point(22, 2)))
player2.addBuilding(level.getBuildingAtPosition(Point(25, 2)))
player2.addBuilding(level.getBuildingAtPosition(Point(27, 4)))
player2.addBuilding(level.getBuildingAtPosition(Point(30, 4)))
player2.addBuilding(level.getBuildingAtPosition(Point(26, 5)))
player2.addBuilding(level.getBuildingAtPosition(Point(27, 5)))
player2.addBuilding(level.getBuildingAtPosition(Point(28, 5)))
player2.addBuilding(level.getBuildingAtPosition(Point(27, 6)))
player2.addBuilding(level.getBuildingAtPosition(Point(26, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(28, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(29, 8)))
player2.addBuilding(level.getBuildingAtPosition(Point(30, 8)))
player2.addBuilding(level.getBuildingAtPosition(Point(25, 9)))
player2.addBuilding(level.getBuildingAtPosition(Point(26, 9)))
