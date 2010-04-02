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
reef                = TerrainType('Reef',          2,  1, hideUnits = True)
cityTerrain         = TerrainType('City',          3,  1)
baseTerrain         = TerrainType('Base',          3,  1)
headquartersTerrain = TerrainType('Headquarters',  4,  1)

# Add the terrain types to the database
database.terrainTypes.extend([road, plains, forest, mountain, river, bridge, shoal, sea, reef, cityTerrain, baseTerrain, headquartersTerrain])


#================================================================================
# Unit types

# name, cost, movementPoints, vision, maxAmmunition
infantery  = UnitType('Infantery',     1000,   3,  2,  0, canCapture = True)
mech       = UnitType('Mech',          1000,   3,  2,  0, canCapture = True)
recon      = UnitType('Recon',         1000,   3,  2,  0)
apc        = UnitType('APC',           1000,   3,  2,  0, canSupply = True)
antiAir    = UnitType('Anti-Air',      1000,   3,  2,  0)
tank       = UnitType('Tank',          1000,   3,  2,  0)
mediumTank = UnitType('Medium Tank',   1000,   3,  2,  0)
heavyTank  = UnitType('Heavy Tank',    1000,   3,  2,  0)
artillery  = UnitType('Artillery',     1000,   3,  2,  0, minRange = 2, maxRange = 3, canFireAfterMove = False, canRetaliate = False)
rocket     = UnitType('Rocket',        1000,   3,  2,  0, minRange = 3, maxRange = 5, canFireAfterMove = False, canRetaliate = False)
# TODO: Ships, aircraft!

# Add the unit types to the database
database.unitTypes.extend([infantery, mech, recon, apc, antiAir, tank, mediumTank, heavyTank, artillery, rocket])

# Vision overrides
infantery.overrideVisionForTerrainType(mountain, 4)
mech.overrideVisionForTerrainType(mountain, 4)

# Movement cost overrides
# Only infantery can cross mountains and rivers - and mechs are faster on mountains than normal infantery
infantery.overrideMovementCostForTerrainType(mountain, 2)
infantery.overrideMovementCostForTerrainType(river, 1)
mech.overrideMovementCostForTerrainType(mountain, 1)
mech.overrideMovementCostForTerrainType(river, 1)
# Wheeled units have more trouble traveling across plains and forested ground
recon.overrideMovementCostForTerrainType(plains, 2)
recon.overrideMovementCostForTerrainType(forest, 3)
apc.overrideMovementCostForTerrainType(plains, 2)
apc.overrideMovementCostForTerrainType(forest, 3)
rocket.overrideMovementCostForTerrainType(plains, 2)
rocket.overrideMovementCostForTerrainType(forest, 3)

# Transporting
apc.setMaximumTransportSlots(1)
apc.canTransport(infantery, 1)
apc.canTransport(mech, 1)

# Damage tables
primaryDamageTable =   [[0,   0,   0,   0,   0,   0,   0,   0,   0,   0  ],
                        [0,   0,   85,  75,  65,  55,  15,  15,  70,  85 ],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0  ],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0  ],
                        [105, 105, 60,  50,  45,  25,  10,  5,   50,  55 ],
                        [0,   0,   85,  75,  65,  55,  15,  15,  70,  80 ],
                        [0,   0,   105, 105, 105, 85,  55,  45,  105, 105],
                        [0,   0,   125, 125, 115, 105, 75,  55,  115, 125],
                        [90,  85,  80,  70,  75,  70,  45,  40,  75,  80 ],
                        [95,  90,  90,  80,  85,  80,  55,  50,  80,  85 ]]

secondaryDamageTable = [[55,  45,  12,  14,  5,   5,   1,   1,   15,  25 ],
                        [65,  55,  18,  20,  6,   6,   1,   1,   32,  35 ],
                        [70,  65,  35,  45,  4,   6,   1,   1,   45,  55 ],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0  ],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0  ],
                        [75,  70,  40,  45,  6,   6,   1,   1,   45,  55 ],
                        [105, 95,  45,  45,  10,  8,   1,   1,   45,  55 ],
                        [125, 115, 65,  45,  17,  10,  1,   1,   65,  75 ],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0  ],
                        [0,   0,   0,   0,   0,   0,   0,   0,   0,   0  ]]

for i in xrange(len(database.unitTypes)):
	for j in xrange(len(database.unitTypes)):
		unitType = database.unitTypes[i]
		targetUnitType = database.unitTypes[j]
		unitType.setDamageAgainst(targetUnitType, primaryDamageTable[i][j], secondaryDamageTable[i][j])


#================================================================================
# Building types

city         = BuildingType('City',           1000)
base         = BuildingType('Base',           1000)
headquarters = BuildingType('Headquarters',   1000)

# Add the building types to the database
database.buildingTypes.extend([city, base, headquarters])

# Bases can build ground units
for unitType in [infantery, mech, recon, apc, antiAir, tank, mediumTank, heavyTank, artillery, rocket]:
	base.canBuild(unitType)

# Associate buildings with their respective terrain types
cityTerrain.buildingType         = city
baseTerrain.buildingType         = base
headquartersTerrain.buildingType = headquarters
