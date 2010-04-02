import os
import sys
from PIL import Image

if len(sys.argv) < 8:
	print '==============================================================='
	print 'Use the the following arguments to process a tilesheet:'
	print '    to_tiles.py [output folder] [spritesheet] [type] [bordering]'
	print '    [transition] [tile width] [tile height]'
	print ''
	print 'For example:'
	print '    to_tiles.py sea.png 3 2,3,4 0,5 16 16'
	print '==============================================================='
	exit()

outputFolder = sys.argv[1]
filename = sys.argv[2]
tileType = sys.argv[3]
bordering = sys.argv[4]
transition = sys.argv[5]
tileWidth = int(sys.argv[6])
tileHeight = int(sys.argv[7])

def saveTile(path, image, corner, x, y, tileWidth, tileHeight, tileType, a, b, c):
	filename = path + tileType + ' ' + corner + ' ' + a + ' ' + b + ' ' + c + '.png'
	tile = image.crop((x, y, x + tileWidth, y + tileHeight))
	tile.load()
	tile.save(filename)
#

spritesheet = Image.open(filename)

# Generate the corner tiles
saveTile(outputFolder, spritesheet, 'tl',  0,  0, tileWidth, tileHeight, tileType, transition, 'x', transition)
saveTile(outputFolder, spritesheet, 'tl', 32,  0, tileWidth, tileHeight, tileType, bordering, 'x', transition)
saveTile(outputFolder, spritesheet, 'tl',  0, 32, tileWidth, tileHeight, tileType, transition, 'x', bordering)
saveTile(outputFolder, spritesheet, 'tl', 64, 64, tileWidth, tileHeight, tileType, bordering, 'x', bordering)

saveTile(outputFolder, spritesheet, 'tr', 80,  0, tileWidth, tileHeight, tileType, transition, 'x', transition)
saveTile(outputFolder, spritesheet, 'tr', 16, 32, tileWidth, tileHeight, tileType, bordering, 'x', transition)
saveTile(outputFolder, spritesheet, 'tr', 48,  0, tileWidth, tileHeight, tileType, transition, 'x', bordering)
saveTile(outputFolder, spritesheet, 'tr', 16, 64, tileWidth, tileHeight, tileType, bordering, 'x', bordering)

saveTile(outputFolder, spritesheet, 'br', 80, 80, tileWidth, tileHeight, tileType, transition, 'x', transition)
saveTile(outputFolder, spritesheet, 'br', 48, 16, tileWidth, tileHeight, tileType, bordering, 'x', transition)
saveTile(outputFolder, spritesheet, 'br', 16, 48, tileWidth, tileHeight, tileType, transition, 'x', bordering)
saveTile(outputFolder, spritesheet, 'br', 16, 16, tileWidth, tileHeight, tileType, bordering, 'x', bordering)

saveTile(outputFolder, spritesheet, 'bl',  0, 80, tileWidth, tileHeight, tileType, transition, 'x', transition)
saveTile(outputFolder, spritesheet, 'bl',  0, 48, tileWidth, tileHeight, tileType, bordering, 'x', transition)
saveTile(outputFolder, spritesheet, 'bl', 32, 16, tileWidth, tileHeight, tileType, transition, 'x', bordering)
saveTile(outputFolder, spritesheet, 'bl', 64, 16, tileWidth, tileHeight, tileType, bordering, 'x', bordering)