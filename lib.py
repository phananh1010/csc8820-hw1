def log(m):
    if len(m) > 0:
        print m
        
def log_prefix(prefix, m):
    if len(m) > 0:
        print '{} {}'.format(prefix, m)