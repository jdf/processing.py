import unittest
    
def return_twelve():
	return 12

class TestTwelveness(unittest.TestCase):
    def test_base(self):
        self.assertEqual(12, return_twelve())

suite = unittest.TestLoader().loadTestsFromTestCase(TestTwelveness)
unittest.TextTestRunner(verbosity=0).run(suite)
print 'OK'
exit()