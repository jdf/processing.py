helloworld = loadStrings("strings.txt")
assert helloworld[0] == 'hello'
assert helloworld[1] == 'world'

helloworld = loadStrings(createReader("strings.txt"))
assert helloworld[0] == 'hello'
assert helloworld[1] == 'world'

expected = 'hello\nworld\n'
for i, c in enumerate(loadBytes("strings.txt")):
    assert c == ord(expected[i]) 

o = loadJSONObject("object.json")
assert o.getString('phrase') == 'hello world'
assert o.getInt('amount') == 42

from java.io import File

o = loadJSONObject(File("testing/resources/data/object.json"))
assert o.getString('phrase') == 'hello world'
assert o.getInt('amount') == 42

a = loadJSONArray("array.json")
assert a.getString(0) == 'hello'
assert a.getString(1) == 'world'

a = loadJSONArray(File("testing/resources/data/array.json"))
assert a.getString(0) == 'hello'
assert a.getString(1) == 'world'

expected = ['hello', 'world']
helloworld = loadStrings(createInput("strings.txt"))
assert helloworld[0] == 'hello'
assert helloworld[1] == 'world'

helloworld = loadStrings(createInput(File("testing/resources/data/strings.txt")))
assert helloworld[0] == 'hello'
assert helloworld[1] == 'world'

print 'OK'
exit()
