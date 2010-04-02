

# Convenience function for debugging
def printMemberVariables(o):
	if hasattr(o, '__dict__'):
		maxkeylen = max([len(key) for key in o.__dict__])
		for key in o.__dict__:
			print key.ljust(maxkeylen + 2, '.') + str(o.__dict__[key])
	elif hasattr(o, '__slots__'):
		maxkeylen = max([len(key) for key in o.__slots__])
		for key in o.__slots__:
			print key.ljust(maxkeylen + 2, '.') + str(eval('o.' + key))
	else:
		print 'No dictionary or slots available for object ' + str(o) + '!'
#