#================================================================================
# Level info
level.name = 'Bean Island'
level.playerCount = 2

#================================================================================
# Terrain data
level.setTileData( [[7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
                    [7,  7,  7,  7,  7,  1,  1,  7,  7,  7,  1,  3,  7,  7,  7,  7],
                    [7,  7,  1,  1,  3,  2,  2,  2,  2,  2,  2,  3,  3,  1,  7,  7],
                    [7,  1,  1,  3,  3,  1,  1,  1,  1,  1,  1,  3,  3,  1,  1,  7],
                    [7,  9,  9,  3,  3,  9,  9,  9,  9,  9,  9,  3,  3,  9,  9,  7],
                    [7,  1,  1,  1,  3,  0,  0,  0,  0,  0,  0,  3,  1,  1,  1,  7],
                    [7,  10, 1,  10, 3,  0,  1,  3,  3,  1,  0,  3,  10, 1,  10, 7],
                    [7,  11, 10, 0,  3,  0,  9,  3,  3,  9,  0,  3,  0,  10, 11, 7],
                    [7,  10, 2,  0,  3,  0,  1,  3,  3,  1,  0,  3,  0,  2,  10, 7],
                    [7,  1,  1,  0,  0,  0,  9,  3,  3,  9,  0,  0,  0,  1,  1,  7],
                    [7,  9,  9,  1,  2,  2,  3,  3,  3,  3,  2,  2,  2,  9,  9,  7],
                    [7,  7,  7,  1,  1,  1,  1,  1,  7,  1,  1,  1,  3,  1,  7,  7],
                    [7,  7,  7,  7,  1,  1,  7,  7,  7,  7,  7,  1,  7,  7,  7,  7],
                    [7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
                    [7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7]] )

#================================================================================
# Player starting buildings
player1 = level.addPlayer()
player1.addBuilding(level.getBuildingAtPosition(Point(1, 4)))
player1.addBuilding(level.getBuildingAtPosition(Point(2, 4)))
player1.addBuilding(level.getBuildingAtPosition(Point(1, 6)))
player1.addBuilding(level.getBuildingAtPosition(Point(3, 6)))
player1.addBuilding(level.getBuildingAtPosition(Point(1, 7)))
player1.addBuilding(level.getBuildingAtPosition(Point(2, 7)))
player1.addBuilding(level.getBuildingAtPosition(Point(6, 7)))
player1.addBuilding(level.getBuildingAtPosition(Point(1, 8)))
player1.addBuilding(level.getBuildingAtPosition(Point(6, 9)))
player1.addBuilding(level.getBuildingAtPosition(Point(1, 10)))
player1.addBuilding(level.getBuildingAtPosition(Point(2, 10)))

player2 = level.addPlayer()
player2.addBuilding(level.getBuildingAtPosition(Point(13, 4)))
player2.addBuilding(level.getBuildingAtPosition(Point(14, 4)))
player2.addBuilding(level.getBuildingAtPosition(Point(12, 6)))
player2.addBuilding(level.getBuildingAtPosition(Point(14, 6)))
player2.addBuilding(level.getBuildingAtPosition(Point(9, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(13, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(14, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(14, 8)))
player2.addBuilding(level.getBuildingAtPosition(Point(9, 9)))
player2.addBuilding(level.getBuildingAtPosition(Point(13, 10)))
player2.addBuilding(level.getBuildingAtPosition(Point(14, 10)))
