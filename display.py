from prettytable import PrettyTable
from operator import itemgetter
from helpers import *


def print_line(level, tag, args):
    """ Print the formatted line of level, tag, and arguments """
    print("<-- %s|%s|%s|%s" % (level, tag, valid_tag(level, tag), args))


def print_indi(individual):
    """ Print individuals """
    for row in sorted(individual, key=itemgetter("ID")):
        print(row["ID"] + " : " + row["NAME"])


def print_fam(individual, family):
    """ Print families """
    for row in sorted(family, key=itemgetter("ID")):
        print(row["ID"] + " : " +
              row["HUSB"] + ":" + get_name(individual, row["HUSB"]) +
              " and " +
              row["WIFE"] + ":" + get_name(individual, row["WIFE"]))


def print_table(individual, family):
    """ Print table of individuals and families """
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
                          row["HUSB"] + ":" + get_name(individual, row["HUSB"]),
                          row["WIFE"] + ":" + get_name(individual, row["WIFE"]),
                          row["CHIL"]])

    print(families)