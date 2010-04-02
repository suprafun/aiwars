# Binds sprites to terrain types, and associates a (x, y, width, height) bounding box with them, to avoid overlap.

# Plains
rules.setSpriteCount('Plains', 2, 5)
rules.addRule('Plains', 'grass_1.png', ( 1,  1,  2,  4))
rules.addRule('Plains', 'grass_2.png', ( 1,  1,  4,  2))
rules.addRule('Plains', 'grass_3.png', ( 1,  1,  5,  2))
rules.addRule('Plains', 'grass_4.png', ( 1,  1,  5,  2))

# Forest
rules.setSpriteCount('Forest', 3, 6)
rules.addRule('Forest', 'tree_1.png', ( 1, 22,  7,  6))
rules.addRule('Forest', 'tree_2.png', ( 1, 10, 11,  6))
rules.addRule('Forest', 'tree_3.png', ( 1, 12, 16,  6))

# Mountain
rules.setSpriteCount('Mountain', 3, 5)
rules.addRule('Mountain', 'rock_1.png', ( 1,  5, 12,  8))
rules.addRule('Mountain', 'rock_2.png', ( 1,  4,  7,  5))
rules.addRule('Mountain', 'rock_3.png', ( 1,  3, 15,  6))

# City
rules.setSpriteCount('City', 3, 5)
rules.addRule('City', 'apartment_1.png', ( 0,  8, 16, 11))
rules.addRule('City', 'apartment_2.png', ( 0,  5,  9, 15))
rules.addRule('City', 'apartment_3.png', ( 0,  8, 10,  9))