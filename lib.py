import timeit

def log(m):
    if len(m) > 0:
        print m
        
def log_prefix(prefix, m):
    if len(m) > 0:
        print '{} {} #{}'.format(prefix, m, timeit.default_timer()%10000)
        
def log_prefix_template(prefix, m, data):
    if len(m) > 0:
        print '{} {} {}#{}'.format(prefix, m, data, timeit.default_timer()%10000)
        
def last_occurrence(arr, m):
    try:
        return len(arr)  - 1 - arr[::-1].index(m)
    except:
        return -1