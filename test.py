import unittest
import project


class TestEmptyInput(unittest.TestCase):

    def test_empty(self):
        wordMatrix = [[]]
        self.assertEqual(project.process_words(wordMatrix), ([], []))

    def test_dateCompare(self):
        self.assertEqual(project.dateCompare('10 SEP 2017'), 'True')
        self.assertTrue(project.dateCompare('10 SEP 2017'))
        self.assertEqual(project.dateCompare('10 SEP 2018'), 'False')
        self.assertEqual(project.dateCompare('20 SEP 2017'), 'True')
        self.assertNotEqual(project.dateCompare('10 SEP 2017'), 'False')
        self.assertNotEqual(project.dateCompare('10 SEP 2018'), 'True')

    def test_lifeDuration(self):
        self.assertTrue(project.validLifeTime('01 JAN 1980', '01 JAN 2020'))
        self.assertTrue(project.validLifeTime('01 JAN 1985', '01 JAN 2020'))
        self.assertTrue(project.validLifeTime('01 JAN 1990', '01 JAN 2020'))
        self.assertFalse(project.validLifeTime('01 JAN 1980', '01 JAN 2220'))
        self.assertFalse(project.validLifeTime('01 JAN 1500', '01 JAN 2520'))
        self.assertFalse(project.validLifeTime('01 JAN 1000', '01 JAN 2220'))

if __name__ == '__main__':
    unittest.main()
