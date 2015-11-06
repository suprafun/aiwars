# Overview #

The _game database_ stores information about all terrain, unit and building types in the game. It is stored in a separate file, and it's content is serialized and sent to all game clients. A server can load any game database it wants, which makes customized battles fairly easy to set up.


# Format #

The game database is written in Python. The game provides several variables and class names:
  * database - the Game<span />Database instance that is to be filled with data
  * Terrain<span />Type - the Terrain<span />Type class
  * Unit<span />Type - the Unit<span />Type class
  * Building<span />Type - the Building<span />Type class


# Registering a database #

The default server takes a game database filename as one of it's arguments. It will search for it in the databases folder.


# Notes #

The default visualization observer client uses terrain type and unit type names to pick the appropriate sprites. You may want to stick to the default names, or you will have to customize the visualization client somewhat - or provide your own visualization client.