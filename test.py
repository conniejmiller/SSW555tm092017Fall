import unittest
import project


class TestEmptyInput(unittest.TestCase):

    def test_empty(self):
        wordMatrix = [[]]
        self.assertEqual(project.process_words(wordMatrix), ([], []))

    def test_dateCompare(self):
        self.assertEqual(dateCompare('10 SEP 2017'), 'True')
        self.assertTrue(dateCompare('10 SEP 2017'))
        self.assertEqual(dateCompare('10 SEP 2018'), 'False')
        self.assertEqual(dateCompare('20 SEP 2017'), 'False')
        self.assertNotEqual(dateCompare('10 SEP 2017'), 'False')
        self.assertNotEqual(dateCompare('10 SEP 2018'), 'True')
        
if __name__ == '__main__':
    unittest.main()
