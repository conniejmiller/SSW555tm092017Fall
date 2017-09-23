import unittest
import project


class TestEmptyInput(unittest.TestCase):

    def test_empty(self):
        """ Testing the process_words function """
        wordMatrix = [[]]
        self.assertEqual(project.process_words(wordMatrix), ([], []))

    def test_date_compare(self):
        """ Testing the date_compare function  """
        self.assertEqual(project.date_compare('10 SEP 2017'), True)
        self.assertTrue(project.date_compare('10 SEP 2017'), True)
        self.assertEqual(project.date_compare('10 SEP 2018'), False)
        self.assertEqual(project.date_compare('20 SEP 2017'), True)
        self.assertNotEqual(project.date_compare('10 SEP 2018'), True)

    def test_is_deceased(self):
        """ Testing the is_deceased function  """ 
        self.assertEqual(project.is_deceased(''), False) 
        self.assertEqual(project.is_deceased('11 SEP 1998'), True)
        self.assertEqual(project.is_deceased('18 MAR 2007'), True)
        self.assertFalse(project.is_deceased(''), True)
        self.assertTrue(project.is_deceased('18 MAR 2007'), True)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
