

# Client to server
CTS_SET_MODE                  = chr(0)
CTS_SET_NAME                  = chr(1)
CTS_READY                     = chr(2)

CTS_MOVE_UNIT                 = chr(3)
CTS_UNLOAD_UNIT               = chr(4)
CTS_SUPPLY_SURROUNDING_UNITS  = chr(5)
CTS_ATTACK_UNIT               = chr(6)
CTS_BUILD_UNIT                = chr(7)
CTS_CAPTURE_BUILDING          = chr(8)
CTS_HIDE_UNIT                 = chr(9)
CTS_END_TURN                  = chr(10)


# Server to client
STC_DATABASE_DATA             = chr(0)
STC_MAP_DATA                  = chr(1)
STC_GAME_DATA                 = chr(2)
STC_START_GAME                = chr(3)

STC_START_TURN                = chr(4)
STC_END_TURN                  = chr(5)
STC_SITUATION_UPDATE          = chr(6)
STC_RESULT                    = chr(7)
STC_END_GAME                  = chr(8)


# Message-specific values
CLIENT_MODE_PLAYER            = chr(0)   # For clients that want to participate in the match
CLIENT_MODE_OBSERVER          = chr(1)   # For clients that only want to observe the match

SERVER_RESULT_SUCCESS         = chr(0)   # A given move has been completed without interruption, the situation has been updated
SERVER_RESULT_TRAPPED         = chr(1)   # A given move has been interrupted by a hidden enemy unit, the situation has been updated
SERVER_RESULT_INVALID         = chr(2)   # A given move was invalid, the situation has not been updated