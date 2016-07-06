import unittest
from search import search
from sort import bubble, selection

class test_serach(unittest.TestCase):
    def setUp(self):
        self.testclass = search()
        self.l = [2,3,4,56,1,89,56]
    def tearDown(self):
        pass
    def testbinarysearch(self):
        self.assertEqual(self.testclass.binarysearch2(self.l,7),False,'pass')
        self.assertEqual(self.testclass.binarysearch2(self.l,4),True,'pass')

class test_sort(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testbubble(self):
        self.assertEqual(bubble([1,5,2,3,5,7]),[1,2,3,5,5,7],'pass')
        self.assertEqual(selection([1,5,2,3,5,7]),[1,2,3,5,5,7],'pass')


if __name__=="__main__":
    unittest.main()
