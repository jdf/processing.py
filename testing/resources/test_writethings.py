import tempfile
from java.io import File

content = "hello"

# guaranteed to be deleted on close and/or garbage collection
with tempfile.NamedTemporaryFile() as tmpfile:

    w = createOutput(tmpfile.name)
    saveBytes(w, content)
    w.close()
    r = createInput(tmpfile.name)
    data = loadBytes(r)
    r.close()
    assert ''.join([chr(c) for c in data]) == content

    w = createOutput(tmpfile.name)
    saveBytes(w, content)
    w.close()
    r = createInput(tmpfile.name)
    data = loadBytes(r)
    r.close()
    assert ''.join([chr(c) for c in data]) == content

print 'OK'
exit()

