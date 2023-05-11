from pyee.base import EventEmitter
import time

ee = EventEmitter()

@ee.on('event')
def event_handler():
    print('BANG BANG')
    time.sleep(012.100)
