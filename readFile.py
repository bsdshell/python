import re;
f       =     open('/tmp/text.txt')
writer  = open("/tmp/output.txt", "w")
for line in iter(f):
    matchObj = re.search(r'(.*/)([^./]*\.java).*?myfolder="([^"]+)', line)

    if matchObj:
        newstr = matchObj.group(1) + matchObj.group(3) 

        print "replace:[",newstr,"]"
        match = re.search(r'\/\w+\/\.\.', newstr)
        while match:
            newstr = re.sub('\/\w+\/\.\.', "", newstr)
            print "replace:[",newstr,"]"
            match = re.search(r'\/\w+\/\.\.', newstr)

        print "group(1):[",matchObj.group(1),"]"
        print "group(2):[",matchObj.group(2),"]"
        print "group(3):[",matchObj.group(3),"]"
        print "newstr:[",newstr,"]"
        
        splitStr = matchObj.group(3)
        if len(splitStr) > 0:
            if splitStr[len(splitStr) - 1] == '/':
                splitStr = splitStr[:len(splitStr)-1]

        splitStr = splitStr.split('/')
        if len(splitStr) > 0 :
            name = splitStr[len(splitStr)-1]
            print "split:",name

        if len(newstr) > 0  and newstr[len(newstr)-1] == '/':
            newstr = newstr[:len(newstr)-2]
            
        column1     =   newstr[2:]
        column2     =   name
        column3     =   name 
        #format columns
        formatStr   =   '{0:55}  {1:30} {2:10}'.format(column1, column2, column3)
        writer.write(formatStr + "\n") 
        print "-----------------------------------"
    else:
        print "No match"
f.close()
writer.close()
