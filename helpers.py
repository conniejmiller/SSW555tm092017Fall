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


def date_compare(date1, date2):
    """ This routine compares 2 dates in the Exact format 
        and returns true if the early date is before thelater date
        otherwise, returns false
        by default, the later date is set to today.
    """
    early_date = datetime.strptime(date1, '%d %b %Y').date()
    if date2 == '':
        late_date = datetime.now().date()
    else:
        late_date = datetime.strptime(date2, '%d %b %Y').date()

    if early_date < late_date:
        return True
    else:
        return False


def get_name(list, id):
    """ Get the name for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["NAME"]
    return "Unknown"
