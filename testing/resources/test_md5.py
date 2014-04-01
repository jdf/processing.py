import md5

hex = md5.new("Nobody inspects the spammish repetition").hexdigest()
assert hex == 'bb649c83dd1ea5c9d9dec9a18df0ffe9'
print 'OK'
exit()
