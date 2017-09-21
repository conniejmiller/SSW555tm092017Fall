from operator import itemgetter
from prettytable import PrettyTable
from datetime import datetime

FILE_NAME = 'data/baseline_input.ged'


# is this a valid combination?
def valid_tag(level, tag):
    # define valid tags at each level
    valid_tags = {"0": ["INDI", "FAM", "HEAD", "TRLR", "NOTE"],
                  "1": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS",
                        "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
                  "2": ["DATE"]}

    return "Y" if level in valid_tags and tag in valid_tags[level] else "N"


# print the formatted line
def print_line(level, tag, args):
    print("<-- %s|%s|%s|%s" % (level, tag, valid_tag(level, tag), args))


# get name for an individual
def getname(list, id):
    for row in list:
        if row["ID"] == id:
            return row["NAME"]
    return "Unknown"


# process rows in the matrix
def process_words(wordMatrix):
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


# print individuals
def print_indi(individual):
    for row in sorted(individual, key=itemgetter("ID")):
        print(row["ID"] + " : " + row["NAME"])


# print families
def print_fam(individual, family):
    for row in sorted(family, key=itemgetter("ID")):
        print(row["ID"] + " : " +
              row["HUSB"] + ":" + getname(individual, row["HUSB"]) +
              " and " +
              row["WIFE"] + ":" + getname(individual, row["WIFE"]))


# print in table
def print_table(individual, family):
    individuals = PrettyTable(["ID",
                               "NAME",
                               "GENDER",
                               "BIRTHDAY",
                               "DEATH"])
    # One space between column edges and contents (default)
    individuals.padding_width = 1
    individuals.align["NAME"] = "l"  # Left align names
    for row in sorted(individual, key=itemgetter("ID")):
        individuals.add_row([row["ID"],
                             row["NAME"],
                             row["SEX"],
                             row["BIRT"],
                             row["DEAT"]])
    print(individuals)

    families = PrettyTable(["ID",
                            "MARRIED",
                            "DIVORCED",
                            "HUSBAND",
                            "WIFE",
                            "CHILDREN"])
    # One space between column edges and contents (default)
    families.padding_width = 1
    families.align["HUSBAND"] = "1"
    families.align["WIFE"] = "1"

    for row in sorted(family, key=itemgetter("ID")):
        families.add_row([row["ID"],
                          row["MARR"],
                          row["DIV"],
                          row["HUSB"] + ":" + getname(individual, row["HUSB"]),
                          row["WIFE"] + ":" + getname(individual, row["WIFE"]),
                          row["CHIL"]])
    print(families)


# process the file
def process_file():
    words = []

    # read the file and process the rows
    with open(FILE_NAME) as inFile:
        for line in inFile:
            words.append(line.split())

    return words


def dateCompare(a):
    """
    This routine compares a date in the Exact format to the current date
    and returns true if it is prior to today
    otherwise, returns false
    """
    # print (datetime.now())
    new_date = datetime.strptime(a, '%d %b %Y').date()
    # print(new_date)

    if new_date < datetime.now().date():
        return 'True'
    else:
        return 'False'


def validateList(indi_list, fam_list):
    for row in indi_list:
        if not dateCompare(row["BIRT"]):
            print('Error US01: Birth date of ' +
                  row["NAME"] + ' (' + row["ID"] + ') ' +
                  'occurs after the current date.')
        # if death date was defined
        if row["DEAT"] != '' and not dateCompare(row["DEAT"]):
            print('Error US01: Death date of ' +
                  row["NAME"] + ' (' + row["ID"] + ') ' +
                  'occurs after the current date.')

    for row in fam_list:
        # if marriage date was not defined - anomaly
        if row["MARR"] == '':
            print('Anomaly: No marriage date exists for family (' +
                  row["ID"] + ').')
        elif not dateCompare(row["MARR"]):
            print('Error US01: Marriage date of ' +
                  getname(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  getname(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
                  ') occurs after the current date.')

        # if divorce date was defined
        if row["DIV"] != '' and not dateCompare(row["DIV"]):
            print('Error US01: Divorce date of ' +
                  getname(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  getname(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
                  ') occurs after the current date.')


# Main processing function
def main():
    words = process_file()

    individual, family = process_words(words)

    # print_indi(individual)
    # print_fam(individual, family)

    print_table(individual, family)

    # Call validation function here
    # vaidateSomething(individual, family)
    validateList(individual, family)


if __name__ == '__main__':
    main()
