#================================================================================
# Client to server

# Before the game has started (lobby)
CTS_SET_MODE                  = chr(0)   # Sets the mode of the client, see CLIENT_MODE_...
CTS_SET_NAME                  = chr(1)   # Sets the name of the client (player name)
CTS_READY                     = chr(2)   # Marksthe client (player) as ready to start the game

# While the game is going
CTS_MOVE_UNIT                 = chr(3)   # Moves a unit along a specified route
CTS_UNLOAD_UNIT               = chr(4)   # Unloads a unit to a specified destination point
CTS_SUPPLY_SURROUNDING_UNITS  = chr(5)   # Supplies the surrounding units
CTS_ATTACK_UNIT               = chr(6)   # Attacks the specified unit
CTS_BUILD_UNIT                = chr(7)   # Builds the specified unit type
CTS_CAPTURE_BUILDING          = chr(8)   # Captures a building
CTS_HIDE_UNIT                 = chr(9)   # Hides or unhides the unit
CTS_END_TURN                  = chr(10)  # Signals that this client is done with it's turn
# TODO: Add a 'destroy unit' command?


#================================================================================
# Server to client

# Before the game has started (lobby)
STC_DATABASE_DATA             = chr(0)   # Sends terrain, unit and building data to the client
STC_MAP_DATA                  = chr(1)   # Sends level data to the client
STC_GAME_DATA                 = chr(2)   # Sends game rule data to the client
STC_START_GAME                = chr(3)   # Informs clients that the game has started

# While the game is going
STC_START_TURN                = chr(4)   # Tells a client that it is it's turn
STC_END_TURN                  = chr(5)   # Tells a client that it's turn is over
STC_SITUATION_UPDATE          = chr(6)   # Sends situation changes to the client - only changes that this client can see! (observer clients can always see every change)
STC_RESULT                    = chr(7)   # Sends the result of the latest command, see SERVER_RESULT_...
STC_END_GAME                  = chr(8)   # Informs clients that the game is over

# While the game is going, observer-specific messages
STC_PLAYER_STARTED_TURN       = chr(9)   # Tells an observer which players turn has started
STC_PLAYER_ENDED_TURN         = chr(10)  # Tells an observer which players turn has ended


#================================================================================
# Message-specific values

# CTS_SET_MODE
CLIENT_MODE_PLAYER            = chr(0)   # For clients that want to participate in the match
CLIENT_MODE_OBSERVER          = chr(1)   # For clients that only want to observe the match

# STC_RESULT
SERVER_RESULT_SUCCESS         = chr(0)   # A given move has been completed without interruption, the situation has been updated
SERVER_RESULT_TRAPPED         = chr(1)   # A given move has been interrupted by a hidden enemy unit, the situation has been updated
SERVER_RESULT_INVALID         = chr(2)   # A given move was invalid, the situation has not been updated
SERVER_RESULT_NOT_YOUR_TURN   = chr(3)   # The client tried to make a move outside it's turn