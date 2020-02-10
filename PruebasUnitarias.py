import unittest
import configuration 
from selenium import webdriver

 #test acceso Epn (calendario)
class TestAV(unittest.TestCase):
    def testEpn(self):
        #driver = webdriver.Chrome('C:\\drivers\\chromedriver_win32\\chromedriver.exe')
        driver = webdriver.Chrome(executable_path="C:\\drivers\\chromedriver_win32\\chromedriver.exe")
        driver.get('https://educacionvirtual.epn.edu.ec')

        titleOfEwbPage=driver.title

        self.assertTrue(titleOfEwbPage == "Google")  #true      
    


#test acceso a trello

class TestTrel(unittest.TestCase):
    def testTrello(self):
        driver = webdriver.Chrome('C:\\drivers\\chromedriver_win32\\chromedriver.exe')
        #driver = webdriver.Chrome(executable_path="C:\drivers\chromedriver_win32\chromedriver.exe")
        driver.get('https://trello.com/es')

        titleOfEwbPage=driver.title

        self.assertTrue(titleOfEwbPage == "Trello")  #true    

#test url trello
class test_check_url(unittest.TestCase):
    def test_trello(self):
        self.assertEqual(configuration.check_for_url('https://recentupcoming'), True)


    
if __name__ == "__main__":
    unittest.main()