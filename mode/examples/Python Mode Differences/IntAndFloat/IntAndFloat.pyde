# The int() and float() functions in Python mode are those
# provided by Python, and they work differently from the
# ones you may know from Processing's Java mode.

# Some uses are the same:

assert int('12') == 12
assert int(12.3) == 12
assert float('8.125') == 8.125

# But there's no form that takes a list of values to
# convert. Instead, do it in Python:
strings = ['12', '47', PI]
ints = [int(x) for x in strings]
assert ints == [12, 47, 3]

# It's easy to build a function that converts something to
# an int, and providea a default value when there's no
# sensible conversion.
def to_int(x, default=0):
    try:
        return int(x)
    except ValueError:
        return default

assert to_int('12') == 12
assert to_int('banana') == 0 
assert to_int('12', -1) == 12 
assert to_int('banana', -1) == -1 
