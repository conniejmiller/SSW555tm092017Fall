import unittest
import project


class TestEmptyInput(unittest.TestCase):

    def test_empty(self):
        """ Testing the process_words function """
        wordMatrix = [[]]
        self.assertEqual(project.process_words(wordMatrix), ([], []))

    def test_dateCompare(self):
        """ Testing the date_compare function  """
        self.assertEqual(project.dateCompare('10 SEP 2017'), True)
        self.assertTrue(project.dateCompare('10 SEP 2017'))
        self.assertEqual(project.dateCompare('10 SEP 2018'), False)
        self.assertEqual(project.dateCompare('20 SEP 2017'), True)
        self.assertNotEqual(project.dateCompare('10 SEP 2017'), False)
        self.assertNotEqual(project.dateCompare('10 SEP 2018'), True)

    def test_is_deceased(self):
        """ Testing the is_deceased function  """ 
        self.assertEqual(project.is_deceased(''), False) 
        self.assertEqual(project.is_deceased('11 SEP 1998'), True)
        self.assertEqual(project.is_deceased('18 MAR 2007'), True)
        self.assertFalse(project.is_deceased(''), True)
        self.assertTrue(project.is_deceased('18 MAR 2007'), True)
        
    def test_lifeDuration(self):
        self.assertTrue(project.validLifeTime('01 JAN 1980', '01 JAN 2020'))
        self.assertTrue(project.validLifeTime('01 JAN 1985', '01 JAN 2020'))
        self.assertTrue(project.validLifeTime('01 JAN 1990', '01 JAN 2020'))
        self.assertFalse(project.validLifeTime('01 JAN 1980', '01 JAN 2220'))
        self.assertFalse(project.validLifeTime('01 JAN 1500', '01 JAN 2520'))
        self.assertFalse(project.validLifeTime('01 JAN 1000', '01 JAN 2220'))


    def test_getAge(self):
        """ Testing the getAge function  """
        self.assertEqual(project.getAge(project.individual, 'p1'), 55)
        self.assertEqual(project.getAge(project.individual, 'p2'), 60)
        self.assertEqual(project.getAge(project.individual, 'p4'), 80)
        self.assertEqual(project.getAge(project.individual, 'p5'), 50)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
