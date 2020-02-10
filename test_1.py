import unittest
import configuration 

class test_check_url(unittest.TestCase):
    def test_trello(self):
        self.assertTrue(configuration.check_for_url('https://recentupcoming'))

        
