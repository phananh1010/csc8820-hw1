import timeit

def log(m):
    if len(m) > 0:
        print m
        
def log_prefix(prefix, m):
    if len(m) > 0:
        print '{}# {} {} '.format(timeit.default_timer()%10000, prefix, m)
        
def log_prefix_template(prefix, m, data):
    if len(m) > 0:
        print '{}# {} {} {}'.format(timeit.default_timer()%10000, prefix, m, data)
        
def last_occurence(arr, m):
    try:
        return len(arr)  - 1 - arr[::-1].index(m)
    except:
        return -1
    
def first_occurence(arr, m):
    try:
        return arr.index(m)
    except:
        return -1