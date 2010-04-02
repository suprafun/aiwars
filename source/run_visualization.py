import sys
from visualization.main import *


if len(sys.argv) < 4:
	print '==============================================================='
	print 'Use the the following arguments to start an AI Wars observer:'
	print '    run_visualization.py [host] [port] [name]'
	print ''
	print 'For example:'
	print '    run_visualization.py localhost 7777 "Observer 1"'
	print '==============================================================='
else:
	main = Main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
	main.run()