# is this a valid combination?
def valid_tag(level, tag):
    # define valid tags at each level
    valid_tags = {"0": ["INDI", "FAM", "HEAD", "TRLR", "NOTE"],
                  "1": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
                  "2": ["DATE"]}

    return "Y" if level in valid_tags and tag in valid_tags[level] else "N"


# print the formatted line
def print_line(level, tag, args):
    print("<-- %s|%s|%s|%s" % (level, tag, valid_tag(level, tag), args))


def process_words(wordMatrix):
    this_type = 'new'
    individual = []
    family = []
    indi_dict = {}
    family_dict = {}

    for words in wordMatrix:
        if len(words) >= 2:
            level = words[0]
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
                individual.append(indi_dict)
                
            elif tag in ("BIRT", "DEAT"):
                indi_dict[tag] = " ".join(other_stuff)
                
            elif tag in ("MARR", "DIV"):
                fam_dict[tag] = " ".join(other_stuff)
            
            elif tag in ("HUSB", "WIFE"):
                fam_dict[tag] = " ".join(other_stuff)
                individual.append(fam_dict)
            
            elif tag == "CHIL":
                fam_dict[tag].append(words[2])
                individual.append(fam_dict)
        else:
            # badly formatted line
            print_line("?", "?", "?")

    # now print the last one
    if this_type == 'INDI':
        individual.append(indi_dict)
    elif this_type == 'FAM':
        family.append(fam_dict)

    return individual, family


def process_file():
    FILE_NAME = '01-project.ged'
    words = []

    # read the file and process the rows
    with open(FILE_NAME) as inFile:
        for line in inFile:
            words.append(line.split())

    individual, family = process_words(words)

    print(individual)
    print(family)


if __name__ == '__main__':
    process_file()