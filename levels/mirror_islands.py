#================================================================================
# Level info
level.name = 'Mirror Islands'
level.supportedDatabases = ['AI Wars']
level.playerCount = 2

#================================================================================
# Terrain data
level.setTileData( [[7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
                    [7,  7,  2,  2,  1,  1,  1,  2,  2,  1,  1,  1,  1,  7,  7,  7,  7,  7,  7,  1,  2,  2,  1,  1,  4,  1,  1,  2,  2,  1,  7,  7],
                    [7,  1,  0,  0,  9,  9,  0,  0,  0,  0,  9,  0,  0,  0,  1,  4,  1,  1,  1,  9,  0,  0,  9,  1,  4,  1,  9,  2,  2,  9,  1,  7],
                    [7,  9,  0,  1,  2,  2,  2,  2,  2,  1,  1,  1,  1,  0,  1,  4,  1,  1,  9,  0,  2,  2,  2,  1,  4,  1,  1,  1,  1,  0,  1,  7],
                    [7,  1,  0,  1,  2,  2,  2,  2,  1,  2,  3,  3,  3,  0,  0,  5,  0,  0,  0,  0,  2,  2,  2,  1,  4,  3,  3,  9,  3,  0,  1,  7],
                    [7,  1,  0,  1,  1,  2,  2,  2,  9,  2,  3,  1,  1,  0,  1,  4,  1,  1,  2,  2,  2,  1,  2,  1,  4,  3,  3,  1,  1,  0,  1,  7],
                    [7, 10,  0, 12,  1,  2,  2,  2,  2,  2,  3,  9,  0,  0,  1,  4,  1,  1,  1,  2,  2,  9,  1,  1,  4,  3,  3,  1, 12,  0, 10,  7],
                    [7, 11, 10,  1,  1,  2,  2,  2,  1,  1,  1,  1,  1,  0,  1,  4,  4,  1,  1,  1,  1,  1,  1,  1,  4,  4,  4,  1,  2, 10, 11,  7],
                    [7, 10,  0, 12,  1,  1,  2,  1,  1,  9,  3,  3,  1,  0,  1,  1,  4,  1,  9,  3,  3,  3,  1,  1,  1,  1,  4,  1,  2,  0, 10,  7],
                    [7,  1,  0,  1,  9,  1,  1,  1,  3,  1,  1,  1,  1,  0,  1,  1,  4,  1,  1,  3,  3,  3,  3,  3,  0,  0,  5,  0,  1,  0,  1,  7],
                    [7,  1,  0,  2,  2,  2,  3,  1,  1,  0,  0,  0,  3,  0,  0,  0,  5,  0,  0,  1,  3,  3,  3,  3,  0,  1,  4,  0,  9,  0,  1,  7],
                    [7,  1,  0,  1,  1,  2,  3,  3,  1,  0,  1,  1,  1,  0,  1,  1,  4,  1,  0,  1,  3,  1,  2,  0,  0,  1,  4,  1,  2,  2,  1,  7],
                    [7,  9,  0,  9,  9,  0,  0,  0,  0,  0,  9,  3,  0,  0,  9,  1,  4,  1,  0,  0,  0,  9,  0,  0,  1,  1,  4,  1,  1,  1,  9,  7],
                    [7,  7,  7,  2,  2,  2,  2,  2,  1,  1,  2,  2,  1,  7,  7,  7,  7,  7,  7,  2,  2,  2,  2,  2,  1,  1,  4,  1,  9,  1,  7,  7],
                    [7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7]] )

#================================================================================
# Player starting buildings
player1 = level.addPlayer()
player1.addBuilding(level.getBuildingAtPosition(Point(1, 6)))
player1.addBuilding(level.getBuildingAtPosition(Point(3, 6)))
player1.addBuilding(level.getBuildingAtPosition(Point(1, 7)))
player1.addBuilding(level.getBuildingAtPosition(Point(2, 7)))
player1.addBuilding(level.getBuildingAtPosition(Point(1, 8)))
player1.addBuilding(level.getBuildingAtPosition(Point(3, 8)))

player2 = level.addPlayer()
player2.addBuilding(level.getBuildingAtPosition(Point(22, 2)))
player2.addBuilding(level.getBuildingAtPosition(Point(26, 2)))
player2.addBuilding(level.getBuildingAtPosition(Point(29, 2)))
player2.addBuilding(level.getBuildingAtPosition(Point(27, 4)))
player2.addBuilding(level.getBuildingAtPosition(Point(21, 6)))
player2.addBuilding(level.getBuildingAtPosition(Point(28, 6)))
player2.addBuilding(level.getBuildingAtPosition(Point(30, 6)))
player2.addBuilding(level.getBuildingAtPosition(Point(18, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(29, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(30, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(30, 8)))
player2.addBuilding(level.getBuildingAtPosition(Point(28, 10)))
player2.addBuilding(level.getBuildingAtPosition(Point(30, 12)))
player2.addBuilding(level.getBuildingAtPosition(Point(28, 13)))
