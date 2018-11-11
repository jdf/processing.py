import tempfile
from java.io import File

content = "hello"

# guaranteed to be deleted on close and/or garbage collection
with tempfile.NamedTemporaryFile() as tmpfile:

    with createOutput(tmpfile.name) as writer:
        saveBytes(writer, content)
    with createInput(tmpfile.name) as reader:
        data = loadBytes(reader)
    assert ''.join([chr(c) for c in data]) == content

    with createOutput(File(tmpfile.name)) as writer:
        saveBytes(writer, content)  
    with createInput(tmpfile.name) as reader:
        data = loadBytes(reader)
    assert ''.join([chr(c) for c in data]) == content

print 'OK'
exit()

