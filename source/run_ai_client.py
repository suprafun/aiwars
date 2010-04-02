import sys
from ai_client.main import *


if len(sys.argv) < 4:
	print '==============================================================='
	print 'Use the the following arguments to start an AI Wars AI client:'
	print '    run_server.py [host] [port] [name]'
	print ''
	print 'For example:'
	print '    run_server.py localhost 7777 "AI Client 1"'
	print '==============================================================='
else:
	main = Main(sys.argv[1], int(sys.argv[2]), sys.argv[3])