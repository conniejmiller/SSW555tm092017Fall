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
with open('01-project.ged', encoding='utf-8') as f:
    for line in f:
        print("-->", line.strip())
        words = line.split()  # split() splits on whitespace and eliminates trailing whitespace
        if len(words) >= 2:
            level = words[0]
            tag = words[1]
            
            if len(words) == 3 and words[2] in ("INDI", "FAM"):
                print_line(level, words[2], words[1])
            else:
                print_line(level, tag, " ".join(words[2:])) # create a string from a sequence of words starting at words[2] separated by " "
        else:
            # badly formatted line
            print_line("?", "?", "?")
            
