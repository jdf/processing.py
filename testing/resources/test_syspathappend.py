import sys
sys.path.append('data')
from foo import victory

def setup():
    pass

def draw():
    assert victory == 'yes'
    print 'OK'
    exit()
