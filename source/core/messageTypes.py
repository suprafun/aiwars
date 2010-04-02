

# Client to server
CTS_SET_MODE                  = chr(1)
CTS_SET_NAME                  = chr(2)
CTS_READY                     = chr(3)

CTS_MOVE_UNIT                 = chr(4)
CTS_UNLOAD_UNIT               = chr(5)
CTS_SUPPLY_SURROUNDING_UNITS  = chr(6)
CTS_ATTACK_UNIT               = chr(7)
CTS_BUILD_UNIT                = chr(8)
CTS_CAPTURE_BUILDING          = chr(9)
CTS_HIDE_UNIT                 = chr(10)
CTS_END_TURN                  = chr(11)


# Server to client
STC_DATABASE_DATA             = chr(1)
STC_MAP_DATA                  = chr(2)
STC_GAME_DATA                 = chr(3)
STC_START_GAME                = chr(4)

STC_START_TURN                = chr(5)
STC_END_TURN                  = chr(6)
STC_SITUATION_UPDATE          = chr(7)
STC_RESULT                    = chr(8)
STC_END_GAME                  = chr(9)


# Message-specific values
CLIENT_MODE_PLAYER            = chr(1)   # For clients that want to participate in the match
CLIENT_MODE_OBSERVER          = chr(2)   # For clients that only want to observe the match

SERVER_RESULT_SUCCESS         = chr(1)   # A given move has been completed without interruption, the situation has been updated
SERVER_RESULT_TRAPPED         = chr(2)   # A given move has been interrupted by a hidden enemy unit, the situation has been updated
SERVER_RESULT_INVALID         = chr(3)   # A given move was invalid, the situation has not been updated