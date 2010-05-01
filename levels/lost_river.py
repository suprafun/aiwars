#================================================================================
# Level info
level.name = 'Lost River'
level.author = 'Advance Wars 2'
level.description = 'Taken from Advance Wars 2, Versus, Classic'

level.supportedDatabases = ['AI Wars']
level.playerCount = 2

#================================================================================
# Terrain data
level.setTileData( [[2,  2,  2,  2,  1,  1,  4,  1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  1,  1,  4,  1,  1,  2,  2],
                    [2,  2,  2,  2,  1,  1,  4,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  1,  2,  1,  1,  1,  1,  1,  4,  1,  2,  2,  2],
                    [2,  2,  1,  1,  1,  1,  4,  1,  1,  9,  9,  9,  9,  9,  9,  9,  1,  1,  1,  1, 12,  1,  9,  9,  9,  9,  1,  5,  1,  1,  1,  2],
                    [2,  2,  1,  9,  1,  1,  4,  4,  1,  1,  1,  1,  1,  1,  1,  1,  1,  4,  4,  4,  4,  4,  1,  1,  1,  1,  1,  4,  1, 12,  1,  2],
                    [2,  2,  9,  1,  1,  1,  1,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  1,  1,  1,  4,  4,  4,  4,  4,  4,  4,  1,  1,  1,  2],
                    [2,  2,  2,  1,  1,  1,  1,  1,  1,  5,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  4,  1,  1,  1,  1,  1,  1,  2],
                    [2,  2,  2,  1,  1,  3,  1,  1,  1,  4,  1,  1,  1,  1,  1,  1,  1,  1,  1,  9,  1,  1,  1,  1,  4,  1,  9,  1,  1, 10, 12,  2],
                    [2,  2,  1,  1,  1,  3,  1,  1,  1,  4,  4,  4,  5,  4,  4,  9,  9,  1,  9,  1,  4,  4,  4,  4,  4,  1,  2,  1, 10, 11, 10,  2],
                    [2,  2, 10,  1, 12,  3,  1,  1,  1,  4,  4,  1,  1,  1,  4,  4,  4,  1,  1,  1,  4,  1,  1,  5,  1,  1,  1,  1,  1, 10,  2,  2],
                    [2, 10, 11, 10,  1,  1,  1,  1,  4,  4,  4,  1,  1,  1,  1,  1,  4,  4,  4,  4,  4,  1,  1,  5,  1,  1,  1,  1, 10,  2,  2,  2],
                    [2,  2, 10,  1,  1,  1,  1,  1,  4,  1,  1,  1,  1,  1,  1,  1,  4,  1,  1,  1,  1,  1,  1,  4,  4,  4,  4,  1,  1,  1,  2,  2],
                    [2,  1,  1,  1,  1,  1,  4,  4,  4,  1,  1,  1,  3,  1,  1,  4,  4,  1,  1,  1,  1,  1,  4,  4,  1,  1,  4,  1,  1,  9,  1,  2],
                    [2,  1,  9,  1,  1,  1,  4,  1,  1,  1,  1,  3,  1,  1,  1,  4,  1,  1,  9,  1,  4,  4,  4,  1,  1,  1,  4,  4,  1,  1,  2,  2],
                    [2,  2,  1,  9,  1,  1,  4,  1,  2,  2,  9,  1,  1, 12,  1,  4,  1,  1,  1,  1,  4,  1,  1,  1,  9,  1,  1,  4,  1,  9,  1,  2],
                    [2,  2,  2,  2,  1,  1,  4,  1,  2,  2,  2,  2,  2,  2,  1,  4,  1,  2,  2,  1,  4,  1,  2,  2,  2,  2,  1,  4,  1,  1,  2,  2]] )

#================================================================================
# Player starting buildings
player1 = level.getPlayerData(0)
player1.addBuilding(level.getBuildingAtPosition(Point(2, 8)))
player1.addBuilding(level.getBuildingAtPosition(Point(4, 8)))
player1.addBuilding(level.getBuildingAtPosition(Point(1, 9)))
player1.addBuilding(level.getBuildingAtPosition(Point(2, 9)))
player1.addBuilding(level.getBuildingAtPosition(Point(3, 9)))
player1.addBuilding(level.getBuildingAtPosition(Point(2, 10)))

player2 = level.getPlayerData(1)
player2.addBuilding(level.getBuildingAtPosition(Point(29, 6)))
player2.addBuilding(level.getBuildingAtPosition(Point(30, 6)))
player2.addBuilding(level.getBuildingAtPosition(Point(28, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(29, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(30, 7)))
player2.addBuilding(level.getBuildingAtPosition(Point(29, 8)))
player2.addBuilding(level.getBuildingAtPosition(Point(28, 9)))