#CODE USAGE for SERVER
import server
import time

print '############################'
print 'SERVER SIDE STARTED'
print '############################'
print '\n'
s = server.Server('Server', 'localhost', 6789, 'localhost', 6666)
time.sleep(1)

s.connect()
time.sleep(1)
s.push_data()
s.close()

print '\n'
print '############################'
print 'SERVER SIDE CLOSING'
print '############################'