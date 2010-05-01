

__guid = 0

# Never return 0 - this allows using 0 as a special case!
def getGUID():
	global __guid
	__guid += 1
	return __guid
#