import unittest
import project


class TestProject(unittest.TestCase):

    def test_empty(self):
        """ Testing the process_words function """
        word_matrix = [[]]
        self.assertEqual(project.process_words(word_matrix), ([], []))

    def test_date_compare(self):
        """ Testing the date_compare function  """
        self.assertEqual(project.date_compare('10 SEP 2017'), True)
        self.assertTrue(project.date_compare('10 SEP 2017'))
        self.assertEqual(project.date_compare('10 SEP 2018'), False)
        self.assertEqual(project.date_compare('20 SEP 2017'), True)
        self.assertNotEqual(project.date_compare('10 SEP 2017'), False)
        self.assertNotEqual(project.date_compare('10 SEP 2018'), True)

    def test_is_deceased(self):
        """ Testing the is_deceased function  """ 
        self.assertEqual(project.is_deceased(''), False) 
        self.assertEqual(project.is_deceased('11 SEP 1998'), True)
        self.assertEqual(project.is_deceased('18 MAR 2007'), True)
        self.assertFalse(project.is_deceased(''), True)
        self.assertTrue(project.is_deceased('18 MAR 2007'), True)
        
    def test_life_duration(self):
        """ Testing if life duration is less than 150 years"""
        self.assertTrue(project.valid_lifetime('01 JAN 1980', '01 JAN 2020'))
        self.assertTrue(project.valid_lifetime('01 JAN 1985', '01 JAN 2020'))
        self.assertTrue(project.valid_lifetime('01 JAN 1000', '01 JAN 1149'))
        self.assertFalse(project.valid_lifetime('01 JAN 1000', '01 JAN 1150'))
        self.assertFalse(project.valid_lifetime('01 JAN 1500', '01 JAN 2520'))
        self.assertFalse(project.valid_lifetime('01 JAN 1000', '01 JAN 2220'))

    def test_get_age(self):
        """ Testing the get_age function  """
        words = project.process_file()
        individual, _ = project.process_words(words)

        self.assertEqual(project.get_age(individual, 'p1'), 55)
        self.assertEqual(project.get_age(individual, 'p2'), 60)
        self.assertEqual(project.get_age(individual, 'p4'), 80)
        self.assertEqual(project.get_age(individual, 'p5'), 51)

    def test_valid_month(self):
        """ Testing is month is valid """
        self.assertTrue(project.valid_month('01 JAN 1980'))
        self.assertTrue(project.valid_month('01 FEB 1980'))
        self.assertTrue(project.valid_month('01 MAR 1980'))
        self.assertFalse(project.valid_month('01 JAM 1980'))
        self.assertFalse(project.valid_month('01 ABC 1980'))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
