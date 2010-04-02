import struct
from point import *


def loadFromPythonFile(level, filename):
	execfile(filename, {'level': level, 'Point': Point})
	
	if not level.gameDatabase.name in level.supportedDatabases:
		print 'Level [' + level.name + '] can\'t be played with database [' + level.gameDatabase.name + ']!'
		level.reset()
#

def loadFromAwmFile(level, filename):
	print '.awm loader not implemented yet!'
#

def loadFromAwsFile(level, filename):
	levelfile = open(filename, 'rb')
	data = levelfile.read()
	levelfile.close()
	
	if not data.startswith('AWSMap001\x00'):
		print 'Invalid .aws file!'
		return
	
	# .aws file layout:
	# header (AWSmap001\x00), 10 bytes
	# x, y - 2 bytes
	# tileset - 1 byte
	# tile data - 2 bytes per tile, collumns first (that is, the order is (0, 0), (0, 1), (1, 0), (1, 1), not (0, 0), (1, 0), (0, 1), (1, 1)) -- likely little endian
	# unit data - 2 bytes per tile, collumns first
	# name string - little endian unsigned int first, then that number of characters (bytes) -- so at least 4 bytes
	# author string - same format as name string
	# description string - same format as name string
	
	width = ord(data[10])
	height = ord(data[11])
	# Ignoring tileset - we've got custom visualization anyway
	
	
	# Parse level terrain data
	readpos = 13
	tiles = []
	players = {}
	for x in xrange(width):
		for y in xrange(height):
			if x == 0:
				tiles.append([])
			awsTile = ord(data[readpos]) + 256 * ord(data[readpos + 1])
			readpos += 2
			
			if not __terrainMapping.has_key(awsTile):
				print 'tile', awsTile, 'is not recognized (at', x, y, ')'
				continue
			(terrainTypeName, team, description) = __terrainMapping[awsTile]
			terrainType = level.gameDatabase.getTerrainTypeByName(terrainTypeName)
			terrainTypeIndex = level.gameDatabase.getIndexOfTerrainType(terrainType)
			tiles[y].append(terrainTypeIndex)
			
			# Store player building data, we can only add buildings once the level has processed the tile data
			if team != None:
				if not players.has_key(team):
					players[team] = []
				players[team].append((x, y))
	level.setTileData(tiles)
	
	
	# Set up players and their starting buildings
	teams = [team for team in players.keys()]
	teams.sort()
	for team in teams:
		player = level.addPlayer()
		for (x, y) in players[team]:
			player.addBuilding(level.getBuildingAtPosition(Point(x, y)))
	
	
	# TODO: Load units!
	print '.aws loader not fully implemented yet: units are ignored!'
	readpos += (width * height * 2)
	
	
	# Read name, author and description - those strings happen to have the same format as AI Wars' string serialization, except that they use little endianness
	
	level.name = __getStringFromData(data, readpos)
	readpos += 4 + len(level.name)
	
	level.author = __getStringFromData(data, readpos)
	readpos += 4 + len(level.author)
	
	level.description = __getStringFromData(data, readpos)
	readpos += 4 + len(level.description)
#

def loadFromAw2File(level, filename):
	print '.aw2 loader not implemented yet!'
#

def loadFromAwdFile(level, filename):
	print '.awd loader not implemented yet!'
#


def __getStringFromData(data, pos):
	(length,) = struct.unpack('<I', data[pos:pos + 4])
	return data[pos + 4:pos + 4 + length]
#


# Terrain type name (see game database), team, description
__terrainMapping = {0: ('Plains', None, 'plains'), \
                    1: ('Road', None, 'road'), \
                    2: ('Bridge', None, 'bridge --'), \
                    3: ('River', None, 'river'), \
                    16: ('Impassable', None, 'pipe'), \
                    30: ('Reef', None, 'reef'), \
                    32: ('Bridge', None, 'bridge |'), \
                    39: ('Shoal', None, 'shoal'), \
                    60: ('Sea', None, 'sea'), \
                    90: ('Forest', None, 'forest'), \
                    150: ('Mountain', None, 'mountain'), \
                    167: ('Plains', None, 'rubble (broken tube)'), \
                    226: ('Impassable', None, 'pipe seam'), \
                    300: ('Headquarters', 0, 'red HQ'), \
                    301: ('City', 0, 'red city'), \
                    302: ('Base', 0, 'red base'), \
                    303: ('Airport', 0, 'red airport'), \
                    304: ('Port', 0, 'red seaport'), \
                    305: ('City', 0, 'red tower'), \
                    306: ('Headquarters', 0, 'red lab'), \
                    310: ('Headquarters', 1, 'blue HQ'), \
                    311: ('City', 1, 'blue city'), \
                    312: ('Base', 1, 'blue base'), \
                    313: ('Airport', 1, 'blue airport'), \
                    314: ('Port', 1, 'blue seaport'), \
                    315: ('City', 1, 'blue tower'), \
                    316: ('Headquarters', 1, 'blue lab'), \
                    320: ('Headquarters', 2, 'green HQ'), \
                    321: ('City', 2, 'green city'), \
                    322: ('Base', 2, 'green base'), \
                    323: ('Airport', 2, 'green airport'), \
                    324: ('Port', 2, 'green seaport'), \
                    325: ('City', 2, 'green tower'), \
                    326: ('Headquarters', 2, 'green lab'), \
                    330: ('Headquarters', 3, 'yellow HQ'), \
                    331: ('City', 3, 'yellow city'), \
                    332: ('Base', 3, 'yellow base'), \
                    333: ('Airport', 3, 'yellow airport'), \
                    334: ('Port', 3, 'yellow seaport'), \
                    335: ('City', 3, 'yellow tower'), \
                    336: ('Headquarters', 3, 'yellow lab'), \
                    340: ('Headquarters', 4, 'black HQ'), \
                    341: ('City', 4, 'black city'), \
                    342: ('Base', 4, 'black base'), \
                    343: ('Airport', 4, 'black airport'), \
                    344: ('Port', 4, 'black seaport'), \
                    345: ('City', 4, 'black tower'), \
                    346: ('Headquarters', 4, 'black lab'), \
                    350: ('Plains', None, 'neutral missile base'), \
                    351: ('City', None, 'neutral city'), \
                    352: ('Base', None, 'neutral base'), \
                    353: ('Airport', None, 'neutral airport'), \
                    354: ('Port', None, 'neutral seaport'), \
                    355: ('City', None, 'neutral tower'), \
                    356: ('Headquarters', None, 'neutral lab'), \
                    900: ('Impassable', None, 'cannon up'), \
                    901: ('Impassable', None, 'cannon left'), \
                    902: ('Impassable', None, 'laser'), \
                    907: ('Impassable', None, 'volcano (0, 0)'), \
                    908: ('Impassable', None, 'volcano (1, 0)'), \
                    909: ('Impassable', None, 'volcano (2, 0)'), \
                    910: ('Impassable', None, 'volcano (3, 0)'), \
                    911: ('Impassable', None, 'giant missile (0, 0)'), \
                    912: ('Impassable', None, 'giant missile (1, 0)'), \
                    913: ('Impassable', None, 'giant missile (2, 0)'), \
                    914: ('Impassable', None, 'giant missile (3, 0)'), \
                    920: ('Impassable', None, 'cannon right'), \
                    921: ('Impassable', None, 'cannon down'), \
                    923: ('Impassable', None, 'crystal?'), \
                    927: ('Impassable', None, 'volcano (0, 1)'), \
                    928: ('Impassable', None, 'volcano (1, 1)'), \
                    929: ('Impassable', None, 'volcano (2, 1)'), \
                    930: ('Impassable', None, 'volcano (3, 1)'), \
                    931: ('Impassable', None, 'giant missile (0, 1)'), \
                    932: ('Impassable', None, 'giant missile (1, 1)'), \
                    933: ('Impassable', None, 'giant missile (2, 1)'), \
                    934: ('Impassable', None, 'giant missile (3, 1)'), \
                    940: ('Impassable', None, 'big cannon down (0, 0)'), \
                    941: ('Impassable', None, 'big cannon down (1, 0)'), \
                    942: ('Impassable', None, 'big cannon down (2, 0)'), \
                    943: ('Impassable', None, 'big cannon up (0, 0)'), \
                    944: ('Impassable', None, 'big cannon up (1, 0)'), \
                    945: ('Impassable', None, 'big cannon up (2, 0)'), \
                    947: ('Impassable', None, 'volcano (0, 2)'), \
                    948: ('Impassable', None, 'volcano (1, 2)'), \
                    949: ('Impassable', None, 'volcano (2, 2)'), \
                    950: ('Impassable', None, 'volcano (3, 2)'), \
                    951: ('Impassable', None, 'giant missile (0, 2)'), \
                    952: ('Impassable', None, 'giant missile (1, 2)'), \
                    953: ('Impassable', None, 'giant missile (2, 2)'), \
                    954: ('Impassable', None, 'giant missile (3, 2)'), \
                    960: ('Impassable', None, 'big cannon down (0, 1)'), \
                    961: ('Impassable', None, 'big cannon down (1, 1)'), \
                    962: ('Impassable', None, 'big cannon down (2, 1)'), \
                    963: ('Impassable', None, 'big cannon up (0, 1)'), \
                    964: ('Impassable', None, 'big cannon up (1, 1)'), \
                    965: ('Impassable', None, 'big cannon up (2, 1)'), \
                    967: ('Impassable', None, 'volcano (0, 3)'), \
                    968: ('Impassable', None, 'volcano (1, 3)'), \
                    969: ('Impassable', None, 'volcano (2, 3)'), \
                    970: ('Impassable', None, 'volcano (3, 3)'), \
                    971: ('Impassable', None, 'giant missile (0, 3)'), \
                    972: ('Impassable', None, 'giant missile (1, 3)'), \
                    973: ('Impassable', None, 'giant missile (2, 3)'), \
                    974: ('Impassable', None, 'giant missile (3, 3)'), \
                    980: ('Impassable', None, 'big cannon down (0, 2)'), \
                    981: ('Impassable', None, 'big cannon down (1, 2)'), \
                    982: ('Impassable', None, 'big cannon down (2, 2)'), \
                    983: ('Impassable', None, 'big cannon up (0, 2)'), \
                    984: ('Impassable', None, 'big cannon up (1, 2)'), \
                    985: ('Impassable', None, 'big cannon up (2, 2)'), \
                    987: ('Impassable', None, 'fortress (0, 0)'), \
                    988: ('Impassable', None, 'fortress (1, 0)'), \
                    989: ('Impassable', None, 'fortress (2, 0)'), \
                    990: ('Impassable', None, 'fortress (3, 0)'), \
                    991: ('Impassable', None, 'ufo (0, 0)'), \
                    992: ('Impassable', None, 'ufo (1, 0)'), \
                    993: ('Impassable', None, 'ufo (2, 0)'), \
                    994: ('Impassable', None, 'ufo (3, 0)'), \
                    995: ('Impassable', None, 'water ufo (0, 0)'), \
                    996: ('Impassable', None, 'water ufo (1, 0)'), \
                    997: ('Impassable', None, 'water ufo (2, 0)'), \
                    998: ('Impassable', None, 'water ufo (3, 0)'), \
                    1000: ('Impassable', None, 'big laser down (0, 0)'), \
                    1001: ('Impassable', None, 'big laser down (1, 0)'), \
                    1002: ('Impassable', None, 'big laser down (2, 0)'), \
                    1003: ('Impassable', None, 'big crystal? (0, 0)'), \
                    1004: ('Impassable', None, 'big crystal? (1, 0)'), \
                    1005: ('Impassable', None, 'big crystal? (2, 0)'), \
                    1007: ('Impassable', None, 'fortress (0, 1)'), \
                    1008: ('Impassable', None, 'fortress (1, 1)'), \
                    1009: ('Impassable', None, 'fortress (2, 1)'), \
                    1010: ('Impassable', None, 'fortress (3, 1)'), \
                    1011: ('Impassable', None, 'ufo (0, 1)'), \
                    1012: ('Impassable', None, 'ufo (1, 1)'), \
                    1013: ('Impassable', None, 'ufo (2, 1)'), \
                    1014: ('Impassable', None, 'ufo (3, 1)'), \
                    1015: ('Impassable', None, 'water ufo (0, 1)'), \
                    1016: ('Impassable', None, 'water ufo (1, 1)'), \
                    1017: ('Impassable', None, 'water ufo (2, 1)'), \
                    1018: ('Impassable', None, 'water ufo (3, 1)'), \
                    1020: ('Impassable', None, 'big laser down (0, 1)'), \
                    1021: ('Impassable', None, 'big laser down (1, 1)'), \
                    1022: ('Impassable', None, 'big laser down (2, 1)'), \
                    1023: ('Impassable', None, 'big crystal? (0, 1)'), \
                    1024: ('Impassable', None, 'big crystal? (1, 1)'), \
                    1025: ('Impassable', None, 'big crystal? (2, 1)'), \
                    1027: ('Impassable', None, 'fortress (0, 2)'), \
                    1028: ('Impassable', None, 'fortress (1, 2)'), \
                    1029: ('Impassable', None, 'fortress (2, 2)'), \
                    1030: ('Impassable', None, 'fortress (3, 2)'), \
                    1031: ('Impassable', None, 'ufo (0, 2)'), \
                    1032: ('Impassable', None, 'ufo (1, 2)'), \
                    1033: ('Impassable', None, 'ufo (2, 2)'), \
                    1034: ('Impassable', None, 'ufo (3, 2)'), \
                    1035: ('Impassable', None, 'water ufo (0, 2)'), \
                    1036: ('Impassable', None, 'water ufo (1, 2)'), \
                    1037: ('Impassable', None, 'water ufo (2, 2)'), \
                    1038: ('Impassable', None, 'water ufo (3, 2)'), \
                    1040: ('Impassable', None, 'big laser down (0, 2)'), \
                    1041: ('Impassable', None, 'big laser down (1, 2)'), \
                    1042: ('Impassable', None, 'big laser down (2, 2)'), \
                    1043: ('Impassable', None, 'big crystal? (0, 2)'), \
                    1044: ('Impassable', None, 'big crystal? (1, 2)'), \
                    1045: ('Impassable', None, 'big crystal? (2, 2)'), \
                    1047: ('Impassable', None, 'fortress (0, 3)'), \
                    1048: ('Impassable', None, 'fortress (1, 3)'), \
                    1049: ('Impassable', None, 'fortress (2, 3)'), \
                    1050: ('Impassable', None, 'fortress (3, 3)'), \
                    1051: ('Impassable', None, 'ufo (0, 3)'), \
                    1052: ('Impassable', None, 'ufo (1, 3)'), \
                    1053: ('Impassable', None, 'ufo (2, 3)'), \
                    1054: ('Impassable', None, 'ufo (3, 3)'), \
                    1055: ('Impassable', None, 'water ufo (0, 3)'), \
                    1056: ('Impassable', None, 'water ufo (1, 3)'), \
                    1057: ('Impassable', None, 'water ufo (2, 3)'), \
                    1058: ('Impassable', None, 'water ufo (3, 3)')}
#

# Unit type name (see game database), team, description
__unitMapping = {500: ('Infantery', 'red', 'infantery'), \
                 501: ('Medium Tank', 'red', 'md tank'), \
                 502: ('Recon', 'red', 'recon'), \
                 503: ('Artillery', 'red', 'artillery'), \
                 504: ('Anti-Air', 'red', 'a-air'), \
                 505: ('Fighter', 'red', 'fighter'), \
                 506: ('Battle copter', 'red', 'b copter'), \
                 507: ('Battleship', 'red', 'battleship'), \
                 508: ('Lander', 'red', 'lander'), \
                 509: ('Heavy Tank', 'red', 'neo tank'), \
                 510: ('Heavy Tank', 'red', 'war tank'), \
                 511: ('None', 'red', 'pipe runner'), \
                 512: ('None', 'red', 'oozium'), \
                 520: ('Mech', 'red', 'mech'), \
                 521: ('Tank', 'red', 'tank'), \
                 522: ('APC', 'red', 'apc'), \
                 523: ('Rockets', 'red', 'rockets'), \
                 524: ('Missiles', 'red', 'missiles'), \
                 525: ('Bomber', 'red', 'bomber'), \
                 526: ('Transport copter', 'red', 't copter'), \
                 527: ('Cruiser', 'red', 'cruiser'), \
                 528: ('Sub', 'red', 'sub'), \
                 529: ('None', 'red', '?? boat'), \
                 530: ('None', 'red', 'carrier'), \
                 531: ('None', 'red', 'stealth bomber'), \
                 532: ('None', 'red', 'cruise missile'), \
                 540: ('Infantery', 'blue', 'infantery'), \
                 541: ('Medium Tank', 'blue', 'md tank'), \
                 542: ('Recon', 'blue', 'recon'), \
                 543: ('Artillery', 'blue', 'artillery'), \
                 544: ('Anti-Air', 'blue', 'a-air'), \
                 545: ('Fighter', 'blue', 'fighter'), \
                 546: ('Battle copter', 'blue', 'b copter'), \
                 547: ('Battleship', 'blue', 'battleship'), \
                 548: ('Lander', 'blue', 'lander'), \
                 549: ('Heavy Tank', 'blue', 'neo tank'), \
                 550: ('Heavy Tank', 'blue', 'war tank'), \
                 551: ('None', 'blue', 'pipe runner'), \
                 552: ('None', 'blue', 'oozium'), \
                 560: ('Mech', 'blue', 'mech'), \
                 561: ('Tank', 'blue', 'tank'), \
                 562: ('APC', 'blue', 'apc'), \
                 563: ('Rockets', 'blue', 'rockets'), \
                 564: ('Missiles', 'blue', 'missiles'), \
                 565: ('Bomber', 'blue', 'bomber'), \
                 566: ('Transport copter', 'blue', 't copter'), \
                 567: ('Cruiser', 'blue', 'cruiser'), \
                 568: ('Sub', 'blue', 'sub'), \
                 569: ('None', 'blue', '?? boat'), \
                 570: ('None', 'blue', 'carrier'), \
                 571: ('None', 'blue', 'stealth bomber'), \
                 572: ('None', 'blue', 'cruise missile'), \
                 580: ('Infantery', 'green', 'infantery'), \
                 581: ('Medium Tank', 'green', 'md tank'), \
                 582: ('Recon', 'green', 'recon'), \
                 583: ('Artillery', 'green', 'artillery'), \
                 584: ('Anti-Air', 'green', 'a-air'), \
                 585: ('Fighter', 'green', 'fighter'), \
                 586: ('Battle copter', 'green', 'b copter'), \
                 587: ('Battleship', 'green', 'battleship'), \
                 588: ('Lander', 'green', 'lander'), \
                 589: ('Heavy Tank', 'green', 'neo tank'), \
                 590: ('Heavy Tank', 'green', 'war tank'), \
                 591: ('None', 'green', 'pipe runner'), \
                 592: ('None', 'green', 'oozium'), \
                 600: ('Mech', 'green', 'mech'), \
                 601: ('Tank', 'green', 'tank'), \
                 602: ('APC', 'green', 'apc'), \
                 603: ('Rockets', 'green', 'rockets'), \
                 604: ('Missiles', 'green', 'missiles'), \
                 605: ('Bomber', 'green', 'bomber'), \
                 606: ('Transport copter', 'green', 't copter'), \
                 607: ('Cruiser', 'green', 'cruiser'), \
                 608: ('Sub', 'green', 'sub'), \
                 609: ('None', 'green', '?? boat'), \
                 610: ('None', 'green', 'carrier'), \
                 611: ('None', 'green', 'stealth bomber'), \
                 612: ('None', 'green', 'cruise missile'), \
                 620: ('Infantery', 'yellow', 'infantery'), \
                 621: ('Medium Tank', 'yellow', 'md tank'), \
                 622: ('Recon', 'yellow', 'recon'), \
                 623: ('Artillery', 'yellow', 'artillery'), \
                 624: ('Anti-Air', 'yellow', 'a-air'), \
                 625: ('Fighter', 'yellow', 'fighter'), \
                 626: ('Battle copter', 'yellow', 'b copter'), \
                 627: ('Battleship', 'yellow', 'battleship'), \
                 628: ('Lander', 'yellow', 'lander'), \
                 629: ('Heavy Tank', 'yellow', 'neo tank'), \
                 630: ('Heavy Tank', 'yellow', 'war tank'), \
                 631: ('None', 'yellow', 'pipe runner'), \
                 632: ('None', 'yellow', 'oozium'), \
                 640: ('Mech', 'yellow', 'mech'), \
                 641: ('Tank', 'yellow', 'tank'), \
                 642: ('APC', 'yellow', 'apc'), \
                 643: ('Rockets', 'yellow', 'rockets'), \
                 644: ('Missiles', 'yellow', 'missiles'), \
                 645: ('Bomber', 'yellow', 'bomber'), \
                 646: ('Transport copter', 'yellow', 't copter'), \
                 647: ('Cruiser', 'yellow', 'cruiser'), \
                 648: ('Sub', 'yellow', 'sub'), \
                 649: ('None', 'yellow', '?? boat'), \
                 650: ('None', 'yellow', 'carrier'), \
                 651: ('None', 'yellow', 'stealth bomber'), \
                 652: ('None', 'yellow', 'cruise missile'), \
                 660: ('Infantery', 'black', 'infantery'), \
                 661: ('Medium Tank', 'black', 'md tank'), \
                 662: ('Recon', 'black', 'recon'), \
                 663: ('Artillery', 'black', 'artillery'), \
                 664: ('Anti-Air', 'black', 'a-air'), \
                 665: ('Fighter', 'black', 'fighter'), \
                 666: ('Battle copter', 'black', 'b copter'), \
                 667: ('Battleship', 'black', 'battleship'), \
                 668: ('Lander', 'black', 'lander'), \
                 669: ('Heavy Tank', 'black', 'neo tank'), \
                 670: ('Heavy Tank', 'black', 'war tank'), \
                 671: ('None', 'black', 'pipe runner'), \
                 672: ('None', 'black', 'oozium'), \
                 680: ('Mech', 'black', 'mech'), \
                 681: ('Tank', 'black', 'tank'), \
                 682: ('APC', 'black', 'apc'), \
                 683: ('Rockets', 'black', 'rockets'), \
                 684: ('Missiles', 'black', 'missiles'), \
                 685: ('Bomber', 'black', 'bomber'), \
                 686: ('Transport copter', 'black', 't copter'), \
                 687: ('Cruiser', 'black', 'cruiser'), \
                 688: ('Sub', 'black', 'sub'), \
                 689: ('None', 'black', '?? boat'), \
                 690: ('None', 'black', 'carrier'), \
                 691: ('None', 'black', 'stealth bomber'), \
                 692: ('None', 'black', 'cruise missile')}
#