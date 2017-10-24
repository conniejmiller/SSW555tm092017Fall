from validate import *
from display import *
from helpers import *

FILE_NAME = 'data/baseline_input.ged'
TEST_FILE_NAME = 'data/testing.ged'


class Gedcom():
    """
    The loader and handler for GEDCOM files
    """
    def __init__(self, file_name):
        try:
            self.words = self._process_file(file_name)
            self.individual, self.family = self._process_words(self.words)
        except:
            print("Unable to process input file")
            self.words = None
            self.individual = None
            self.family = None

    def _process_words(self, wordMatrix):
        """ Process rows in the matrix """
        this_type = 'new'
        this_tag = 'new'
        individual = []
        family = []
        indi_dict = {}
        fam_dict = {}

        for words in wordMatrix:
            if len(words) >= 2:
                tag = words[1]
                other_stuff = words[2:]

                if len(words) == 3 and words[2] in ("INDI", "FAM"):
                    # print lastline
                    if this_type == 'INDI':
                        individual.append(indi_dict)
                    elif this_type == 'FAM':
                        family.append(fam_dict)

                    if words[2] == "INDI":
                        indi_dict = {"ID": tag,
                                     "NAME": '',
                                     "SEX": '',
                                     "BIRT": '',
                                     "DEAT": ''}
                        this_type = 'INDI'
                    else:
                        fam_dict = {"ID": tag,
                                    "MARR": '',
                                    "HUSB": '',
                                    "WIFE": '',
                                    "CHIL": [],
                                    "DIV": ''}
                        this_type = 'FAM'

                elif tag in ("NAME", "SEX"):
                    indi_dict[tag] = " ".join(other_stuff)

                elif tag in ("BIRT", "DEAT", "MARR", "DIV"):
                    # savethis tag so we can write it after the next row
                    this_tag = tag

                elif tag in ("DATE"):
                    if this_type == 'INDI':
                        indi_dict[this_tag] = " ".join(other_stuff)
                    elif this_type == 'FAM':
                        fam_dict[this_tag] = " ".join(other_stuff)
                    this_tag = 'new'

                elif tag in ("HUSB", "WIFE"):
                    fam_dict[tag] = " ".join(other_stuff)

                elif tag == "CHIL":
                    fam_dict[tag].append(words[2])

        # now print the last one
        if this_type == 'INDI':
            individual.append(indi_dict)
        elif this_type == 'FAM':
            family.append(fam_dict)

        return individual, family

    def _process_file(self, filename):
        """  Process the file """
        words = []

        # read the file and process the rows
        with open(filename) as in_file:
            for line in in_file:
                words.append(line.split())

        return words

    def display(self):
        """Display the contents of the GEDCOM file"""
        print_table(self.individual, self.family)
        list_deceased(self.individual)
        get_recent_deaths(self.individual)
        get_recent_births(self.individual)
        get_living_married(self.family, self.individual)
        list_living_single(self.individual, self.family)

    def validate(self):
        """Validate the contents of the GEDCOM file"""
        validate_dates(self.individual, self.family)
        validate_genders(self.family, self.individual)
        validate_males(self.family, self.individual)
        validate_marriages(self.family, self.individual)


def main():
    """ Main processing function
    """
    gedcom = Gedcom(FILE_NAME)

    gedcom.display()
    gedcom.validate()

if __name__ == '__main__':
    main()
