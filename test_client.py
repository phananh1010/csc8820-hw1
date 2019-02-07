#CODE USAGE for CLIENT
import client
import time

print '############################'
print 'CLIENT SIDE'
print '############################'
print '\n'
c = client.Client('Client', 'localhost', 6666, 'localhost', 6789)
time.sleep(1)
c.connect()

time.sleep(1)



#after receive the push data, should close now
print '\n'
print '############################'
print 'CLIENT SIDE CLOSING'
print '############################'