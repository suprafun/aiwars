

# Client to server
CTS_SET_MODE                  = chr(1)
CTS_SET_NAME                  = chr(2)
CTS_READY                     = chr(3)

CTS_MOVE_UNIT                 = chr(4)
CTS_LOAD_UNIT                 = chr(5)
CTS_UNLOAD_UNIT               = chr(6)
CTS_SUPPLY_SURROUNDING_UNITS  = chr(7)
CTS_ATTACK_UNIT               = chr(8)
CTS_COMBINE_UNITS             = chr(9)
CTS_BUILD_UNIT                = chr(10)
CTS_CAPTURE_BUILDING          = chr(11)
CTS_END_TURN                  = chr(12)


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