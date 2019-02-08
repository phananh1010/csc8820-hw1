class Stats:
    TRY = 1;
    PACKET = 2;
    
    dat = {}
    def __init__(self):
        return
    
    def log(self, label, value=1):
        if label in self.dat:
            self.dat[label] += value
        else:
            self.dat[label] = value