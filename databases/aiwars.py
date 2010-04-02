

database.name = 'AI Wars'

#================================================================================
# Terrain types

# name, cover, movementCost
road                = TerrainType('Road',          0,  1)
plains              = TerrainType('Plains',        1,  1)
forest              = TerrainType('Forest',        2,  1, hideUnits = True)
mountain            = TerrainType('Mountain',      4,  99)
river               = TerrainType('River',         0,  99)
bridge              = TerrainType('Bridge',        0,  1)
shoal               = TerrainType('Shoal',         0,  1)
sea                 = TerrainType('Sea',           0,  99)
reef                = TerrainType('Reef',          1,  99, hideUnits = True)
cityTerrain         = TerrainType('City',          3,  1)
baseTerrain         = TerrainType('Base',          3,  1)
headquartersTerrain = TerrainType('Headquarters',  4,  1)
airportTerrain      = TerrainType('Airport',       3,  1)
dockTerrain         = TerrainType('Dock',          3,  1)

# Add the terrain types to the database
database.terrainTypes.extend([road, plains, forest, mountain, river, bridge, shoal, sea, reef, cityTerrain, baseTerrain, headquartersTerrain, airportTerrain, dockTerrain])



#================================================================================
# Unit types

# name, cost, movementPoints, vision, maxAmmunition
infantery        = UnitType('Infantery',         1000,   3,  2,  0, canCapture = True)
mech             = UnitType('Mech',              3000,   2,  2,  3, canCapture = True)
recon            = UnitType('Recon',             4000,   8,  5,  0)
apc              = UnitType('APC',               5000,   6,  1,  0, canSupply = True)
antiAir          = UnitType('Anti-Air',          8000,   6,  2,  9)
tank             = UnitType('Tank',              7000,   6,  3,  9)
mediumTank       = UnitType('Medium Tank',      16000,   5,  1,  8)
heavyTank        = UnitType('Heavy Tank',       22000,   6,  1,  9)
artillery        = UnitType('Artillery',         6000,   5,  1,  9, minRange = 2, maxRange = 3, canActAfterMoving = False, canRetaliate = False)
rockets          = UnitType('Rockets',          15000,   5,  1,  6, minRange = 3, maxRange = 5, canActAfterMoving = False, canRetaliate = False)
missiles         = UnitType('Missiles',         12000,   4,  5,  6, minRange = 3, maxRange = 5, canActAfterMoving = False, canRetaliate = False)

fighter          = UnitType('Fighter',          20000,   9,  2,  9)
bomber           = UnitType('Bomber',           22000,   7,  2,  9)
battleCopter     = UnitType('Battle copter',     9000,   6,  3,  6)
transportCopter  = UnitType('Transport copter',  5000,   6,  2,  0)

battleShip       = UnitType('Battleship',       28000,   5,  2,  9, minRange = 2, maxRange = 6, canActAfterMoving = False, canRetaliate = False)
cruiser          = UnitType('Cruiser',          18000,   6,  3,  9)
lander           = UnitType('Lander',           12000,   6,  1,  0)
sub              = UnitType('Sub',              20000,   5,  5,  6, canHide = True)

groundUnits = [infantery, mech, recon, apc, antiAir, tank, mediumTank, heavyTank, artillery, rockets, missiles]
aerialUnits = [fighter, bomber, battleCopter, transportCopter]
navalUnits = [battleShip, cruiser, lander, sub]

# Add the unit types to the database
database.unitTypes.extend([infantery, mech, recon, apc, antiAir, tank, mediumTank, heavyTank, artillery, rockets, missiles, \
                           fighter, bomber, battleCopter, transportCopter, \
                           battleShip, cruiser, lander, sub])

# Infantery can look further when standing on tall mountains
infantery.overrideVisionForTerrainType(mountain, 4)
mech.overrideVisionForTerrainType(mountain, 4)

# Only infantery can cross mountains and rivers - and mechs are faster on mountains and rivers than normal infantery. All infantery is relatively fast in forests.
infantery.overrideMovementCostForTerrainType(mountain, 2)
infantery.overrideMovementCostForTerrainType(river, 1)
infantery.overrideMovementCostForTerrainType(forest, 1)
mech.overrideMovementCostForTerrainType(mountain, 1)
mech.overrideMovementCostForTerrainType(river, 1)
mech.overrideMovementCostForTerrainType(forest, 1)

# Wheeled units have more trouble traveling across plains and forested ground
recon.overrideMovementCostForTerrainType(plains, 2)
recon.overrideMovementCostForTerrainType(forest, 3)
apc.overrideMovementCostForTerrainType(plains, 2)
apc.overrideMovementCostForTerrainType(forest, 3)
rockets.overrideMovementCostForTerrainType(plains, 2)
rockets.overrideMovementCostForTerrainType(forest, 3)

# All flying units have a movement cost of 1 for every tile
for unitType in aerialUnits:
	for terrainType in database.terrainTypes:
		unitType.overrideMovementCostForTerrainType(terrainType, 1)
		
# Naval units can't cross land - and only the lander can land on shoal
for unitType in navalUnits:
	for terrainType in database.terrainTypes:
		unitType.overrideMovementCostForTerrainType(terrainType, 99)
	unitType.overrideMovementCostForTerrainType(sea, 1)
	unitType.overrideMovementCostForTerrainType(reef, 2)
lander.overrideMovementCostForTerrainType(shoal, 1)

# Both apc's and transport copters can carry 1 infantery unit
apc.setMaximumTransportSlots(1)
apc.canTransport(infantery, 1)
apc.canTransport(mech, 1)
transportCopter.setMaximumTransportSlots(1)
transportCopter.canTransport(infantery, 1)
transportCopter.canTransport(mech, 1)

# Landers can carry 2 ground units
lander.setMaximumTransportSlots(2)
for unitType in groundUnits:
	lander.canTransport(unitType, 1)

# Cruisers can carry 2 copters
cruiser.setMaximumTransportSlots(2)
cruiser.canTransport(battleCopter, 1)
cruiser.canTransport(transportCopter, 1)

# Damage tables
primaryDamageTable =   [[0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   85,  75,  65,  55,  15,  15,  70,  85,  85,      0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [105, 105, 60,  50,  45,  25,  10,  5,   50,  55,  55,      65,  75,  120, 120,     0,   0,   0,   0],
                        [0,   0,   85,  75,  65,  55,  15,  15,  70,  80,  85,      0,   0,   0,   0,       1,   5,   10,  1],
                        [0,   0,   105, 105, 105, 85,  55,  45,  105, 105, 105,     0,   0,   0,   0,       10,  45,  35,  10],
                        [0,   0,   125, 125, 115, 105, 75,  55,  115, 125, 125,     0,   0,   0,   0,       15,  50,  40,  15],
                        [90,  85,  80,  70,  75,  70,  45,  40,  75,  80,  80,      0,   0,   0,   0,       40,  65,  55,  60],
                        [95,  90,  90,  80,  85,  80,  55,  50,  80,  85,  90,      0,   0,   0,   0,       55,  85,  60,  85],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       100, 100, 120, 120,     0,   0,   0,   0],

                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       55,  100, 100, 100,     0,   0,   0,   0],
                        [110, 110, 105, 105, 95,  105, 95,  90,  105, 105, 105,     0,   0,   0,   0,       75,  85,  95,  95],
                        [0,   0,   55,  60,  25,  55,  25,  20,  65,  65,  65,      0,   0,   0,   0,       25,  55,  25,  25],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],

                        [95,  90,  90,  80,  85,  80,  55,  50,  80,  85,  90,      0,   0,   0,   0,       50,  95,  95,  95],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   90],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       55,  25,  95,  55]]


secondaryDamageTable = [[55,  45,  12,  14,  5,   5,   1,   1,   15,  25,  25,      0,   0,   7,   30,      0,   0,   0,   0],
                        [65,  55,  18,  20,  6,   6,   1,   1,   32,  35,  35,      0,   0,   0,   0,       0,   0,   0,   0],
                        [70,  65,  35,  45,  4,   6,   1,   1,   45,  55,  28,      0,   0,   10,  35,      0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [75,  70,  40,  45,  6,   6,   1,   1,   45,  55,  30,      0,   0,   10,  40,      0,   0,   0,   0],
                        [105, 95,  45,  45,  10,  8,   1,   1,   45,  55,  35,      0,   0,   12,  45,      0,   0,   0,   0],
                        [125, 115, 65,  45,  17,  10,  1,   1,   65,  75,  55,      0,   0,   22,  55,      0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],

                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [75,  75,  30,  20,  6,   6,   1,   1,   25,  35,  35,      0,   0,   65,  95,      0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],

                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       55,  65,  115, 115,     0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,       0,   0,   0,   0,       0,   0,   0,   0]]

for i in xrange(len(database.unitTypes)):
	for j in xrange(len(database.unitTypes)):
		unitType = database.unitTypes[i]
		targetUnitType = database.unitTypes[j]
		unitType.setDamageAgainst(targetUnitType, primaryDamageTable[i][j], secondaryDamageTable[i][j])



#================================================================================
# Building types

# Name, income per turn
city         = BuildingType('City',           1000, canRepairUnitTypes = groundUnits)
base         = BuildingType('Base',           1000, canRepairUnitTypes = groundUnits)
headquarters = BuildingType('Headquarters',   1000, canRepairUnitTypes = groundUnits, critical = True)
airport      = BuildingType('Airport',        1000, canRepairUnitTypes = aerialUnits)
dock         = BuildingType('Dock',           1000, canRepairUnitTypes = navalUnits)

# Add the building types to the database
database.buildingTypes.extend([city, base, headquarters, airport, dock])

# Bases can build ground units
for unitType in groundUnits:
	base.canBuild(unitType)

# Airports can build aerial units
for unitType in aerialUnits:
	airport.canBuild(unitType)

# Docks can build naval units
for unitType in navalUnits:
	dock.canBuild(unitType)

# Associate buildings with their respective terrain types
cityTerrain.buildingType         = city
baseTerrain.buildingType         = base
headquartersTerrain.buildingType = headquarters
airportTerrain.buildingType      = airport
dockTerrain.buildingType         = dock
