#CODE USAGE for SERVER
import router
import time

print '############################'
print 'ROUTER SIDE STARTED'
print '############################'
print '\n'
r = router.Router('Router', ('localhost', 6789, 'localhost', 6666), ('localhost', 9876, 'localhost', 9999))
time.sleep(2)

r.connect()
time.sleep(1)

