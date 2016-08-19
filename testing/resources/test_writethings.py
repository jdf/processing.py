import tempfile
from java.io import File

content = "hello"

# guaranteed to be deleted on close and/or garbage collection
with tempfile.NamedTemporaryFile() as tmpfile:

    writer = createOutput(tmpfile.name)
    saveBytes(writer, content)
    tmpfile.flush()
    reader = createInput(tmpfile.name)
    data = loadBytes(reader)
    assert ''.join([chr(c) for c in data]) == content

    writer = createOutput(File(tmpfile.name))
    saveBytes(writer, content)
    tmpfile.flush()
    reader = createInput(tmpfile.name)
    data = loadBytes(reader)
    assert ''.join([chr(c) for c in data]) == content

print 'OK'
exit()

