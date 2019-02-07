#CODE USAGE for CLIENT
import client
import time

print '############################'
print 'CLIENT SIDE'
print '############################'
print '\n'
c = client.Client('Client', 'localhost', 9999, 'localhost', 9876)
time.sleep(2)
c.connect()

time.sleep(1)

