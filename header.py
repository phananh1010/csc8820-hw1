PACKET_SIZE=9
PACKET_CLOSE = 999999 #this packet notify server that connection can be closed now
TEMPLATE = '{{0:0{}}}'.format(PACKET_SIZE)
WINDOW_NODATA  = -1
WINDOW_HASDATA = 1
DROP_CHANCE = (4+7)*0.1*0.01 #my id is 002349134, Xiang id is 002400397
                  #drop chance = (4 + 7) * 0.01

CLIENT_NAKCOUNT = 2

SLEEP_SEND = 0.050