import unittest
from polical import configuration
from selenium import webdriver

from polical from create_subject import Add_Subject_To_Trello_List
from connection import TrelloConnection


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



#test a�adir una materia a Trello
class Test_Add_Subject_To_Trello_List(unittest.TestCase):
    def test_given_a_new_list_when_add_an_subject_then_it_has_one_element(self):
        subjectsBoard.list_lists()
	subjectsBoard.add_list(subject_name)
        self.assertEqual(1.subjectsBoard.size())



#test mostrar usuario "andres" conectado a Trello
class TestTrelloConnection(unittest.TestCase):
    def test_trello_client(self):
	trelloClient=TrelloConnection()
	user=trelloClient.initialize_trello("andres")
	self.assertEqual("andres", trello_client)



if __name__ == "__main__":
    unittest.main()
