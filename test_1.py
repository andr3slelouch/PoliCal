import unittest
import configuration 

class test_check_url(unittest.TestCase):
    def test_trello(self):
        self.assertEqual(configuration.check_for_url('https://recentupcoming'),True)

        
