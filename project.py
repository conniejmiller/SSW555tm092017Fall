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


def process_words(inFile):
    this_type = 'new'
    individual = []
    family = []
    indi_dict = {}
    family_dict = {}

    while 1:
        line = inFile.readline()
        if not line:
            break
        words = line.split() # split() splits on whitespace and eliminates trailing whitespace

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
                
            elif tag in ("BIRT", "DEAT"):
                line = fp.readline()
                words = line.split()
                indi_dict[tag] = " ".join(words[2:])
                
            elif tag in ("MARR", "DIV"):
                line = fp.readline()
                words = line.split()
                fam_dict[tag] = " ".join(words[2:])
            
            elif tag in ("HUSB", "WIFE"):
                fam_dict[tag] = " ".join(other_stuff)
            
            elif tag == "CHIL":
                fam_dict[tag].append(words[2])
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
    inFile = open(FILE_NAME)

    individual, family = process_words(inFile)


if __name__ == '__main__':
    process_file()
    
    print(individual)
    print(family)
