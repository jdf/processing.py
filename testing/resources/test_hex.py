assert hex(unhex(hex(0xcafebabe))) == 'CAFEBABE'
assert unhex(hex(unhex('0xcafebabe'))) == 0xCAFEBABE
assert hex(unhex(hex(0xdecaf))) == 'DECAF'
assert unhex(hex(unhex('DECAF'))) == 0xDECAF
print 'OK'
exit()