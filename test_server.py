#CODE USAGE for SERVER
import server
import time
import sys


print '############################'
print 'SERVER SIDE STARTED'
print '############################'
print '\n'
s = server.Server('Server', 'localhost', 6666, 'localhost', 6789)
time.sleep(2)

s.connect()
time.sleep(1)
s.push_data()

print 'TOTAL number of TRY: {}'.format(s.stats.dat[s.stats.TRY])