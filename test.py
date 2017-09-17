import unittest
import project


class TestEmptyInput(unittest.TestCase):

    def test_empty(self):
        wordMatrix = [[]]
        self.assertEqual(project.process_words(wordMatrix), ([], []))

if __name__ == '__main__':
    unittest.main()
