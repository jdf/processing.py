assert hex(unhex(hex(0xcafebabe))) == 'CAFEBABE'
assert unhex(hex(unhex('cafebabe'))) == 0xCAFEBABE
assert hex(unhex(hex(0xdecaf))) == '000DECAF'
assert unhex(hex(unhex('DECAF'))) == 0xDECAF
print 'OK'
exit()