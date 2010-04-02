# Binds sprites to terrain types, and associates a (x, y, width, height) bounding box with them, to avoid overlap.

# Plains
rules.addRule('Plains', 'grass_1.png', (-1, -1,  6,  8))
rules.addRule('Plains', 'grass_2.png', (-1, -1,  8,  6))
rules.addRule('Plains', 'grass_3.png', (-1, -1,  9,  6))
rules.addRule('Plains', 'grass_4.png', (-1, -1,  9,  6))

# Forest
rules.addRule('Forest', 'tree_1.png', (-1, 10, 20, 10))
rules.addRule('Forest', 'tree_2.png', (-1,  8, 15, 10))
rules.addRule('Forest', 'tree_3.png', (-1, 20,  9, 10))

# City
rules.addRule('City', 'apartment_1.png', (-2,  6, 20, 15))
rules.addRule('City', 'apartment_2.png', (-2,  3, 13, 19))
rules.addRule('City', 'apartment_3.png', (-2,  6, 14, 13))