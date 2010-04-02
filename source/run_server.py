import sys
from server.main import *


if len(sys.argv) != 5:
	print '==============================================================='
	print '| Use the the following arguments to start an AI Wars server: |'
	print '|     run_server.py [host] [port] [levelfile] [databasefile]  |'
	print '|                                                             |'
	print '| For example:                                                |'
	print '|     run_server.py localhost 7777 spann_island.py aiwars.py  |'
	print '==============================================================='
else:
	main = Main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])