class Foo(str):
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return self.arg
    
foo = Foo('cosmic')
print foo
print str(12)
print str([12,13])