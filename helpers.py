from math import floor
from datetime import datetime


def is_deceased(row_death):
    """ Check if an individual is dea and return a Boolean val """
    try:
        row_death = str(row_death)
        if not row_death:
            return False
        else:
            return True
    except ValueError:
        print('Invalid type.')


def list_deceased(indi_list):
    """ This function loops through the individual list and prints
        names of deceased people
    """
    for row in indi_list:
        if is_deceased(row["DEAT"]):
            print('US29: Deceased: {0}, {1}'.format(row["NAME"], row['DEAT']))


def date_compare(a):
    """ This routine compares a date in the Exact format to the current date
        and returns true if it is prior to today
        otherwise, returns false
    """
    # print (datetime.now())
    new_date = datetime.strptime(a, '%d %b %Y').date()
    # print(new_date)

    if new_date < datetime.now().date():
        return True
    else:
        return False


def get_name(list, id):
    """ Get the name for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["NAME"]
    return "Unknown"