# timer.py

import time

class timer:
    TIMER_STOP=-1
    _TIMER={}
    
    def __init__(self, _interval):
        self.start_time = self.TIMER_STOP
        self.interval = _interval
    def start(self, seq):
        self._TIMER[seq]=time.time() 

    def get_time(self):
        return time.time()

    def overtime(self, seq):
        if seq >= len(self._TIMER):
            seq-=1
        if time.time()-self._TIMER[seq] > self.interval:
            return True
        else:
            return False
