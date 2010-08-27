This is a little utility to give you the "human readable" color name given a hex
value. Heavily based (one might even just call it a port...) on
[ntc.js](http://chir.ag/projects/ntc/) by Chirag Mehta.

Usage
=====

+ As a library:

    \>\>\> from NameThatColor import NameThatColor
    
    \>\>\> Namer = NameThatColor()
    
    \>\>\> Namer.name('FFFFFF')
    
    Match(hex_value='#FFFFFF', name='White', exact=True, original='#FFFFFF')
    
    \>\>\> Namer.name('#FFFFFF')
    
    Match(hex_value='#FFFFFF', name='White', exact=True, original='#FFFFFF')
    
    \>\>\> Namer.name('aabbcc')
    
    Match(hex_value='#ADBED1', name='Casper', exact=False, original='#AABBCC')
+ As a program:
    $ namethatcolor ffffff
    
    {"match_hex": "#FFFFFF", "match_name": "White"}
