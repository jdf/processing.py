import time

def setup():
	size(10, 10)

n = 0

def func1():
	global n
	n += 1

def func2():
	global n
	n += 4

def draw():
	noLoop()
	thread("func1")
	while n < 1:
		time.sleep(0.02)
	thread(func2)
	while n < 5:
		time.sleep(0.02)
	print('OK')
	exit()
