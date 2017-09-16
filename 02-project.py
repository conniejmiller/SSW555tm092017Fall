# is this a valid combination?
def valid_tag(level,tag):
    # define valid tags at each level
    valid_tags = {"0": ["INDI", "FAM", "HEAD", "TRLR", "NOTE"],
                  "1": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
                  "2": ["DATE"]}
                  
    return "Y" if level in valid_tags and tag in valid_tags[level] else "N"
    
# print the formatted line
def print_line(level, tag, args):
    print("<-- %s|%s|%s|%s" % (level, tag, valid_tag(level, tag), args))

# read the file and process the rows  
fp = open('01-project.ged', encoding='utf-8')

individual = []
family = []
    
while 1:
    line = fp.readline()
    if not line:
        break
    words = line.split()  # split() splits on whitespace and eliminates trailing whitespace

    if len(words) >= 2:
        level = words[0]
        tag = words[1]
        other_stuff = words[2:]
   
        if len(words) == 3 and words[2] in ("INDI", "FAM"):
                
            if words[2] == "INDI":
                indi_dict = {"ID":tag,"NAME":'',"SEX":'',"BIRT":'',"DEAT":''}
                this_type = 'INDI'
                individual.append(indi_dict)
            else:
                fam_dict = {"ID":tag,"MARR":'',"HUSB":'',"WIFE":'',"CHIL":[],"DIV":''}
                this_type = 'FAM'
                family.append(fam_dict)
            
        else:
            if this_type == 'INDI':
                print ("INDI")
            else:
                print ("FAM")

    else:
        # badly formatted line
        print_line("?", "?", "?")

print (individual)
print ('')
print (family)
