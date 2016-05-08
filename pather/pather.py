#!/usr/bin/python
import re;
import os;
import sys;

pathfile    = "/Users/cat/myfile/github/python/pather/path.txt"
pathWriter  = open(pathfile, "r+")

plist = []
columnList = []
arglist = sys.argv;

def removeDuplicate(list, str):
    tmpList = list[:]
    for line in tmpList:
        split = re.split(':', line)
        if len(split) > 1 and split[1] == str:
            list.remove(line)

    return list 


for line in iter(pathWriter):
    plist.append(line)

# push path to stack
if len(arglist) == 1:
    newIndex = 0
    if  len(plist) > 0:
        tmpListList = plist[:];

        currPath = os.getcwd() + '\n'
        uniqueList = removeDuplicate(plist, currPath)

        pathWriter.seek(0)
        pathWriter.truncate()
        index = 0
        for item in uniqueList:
            split = re.split(":", item)
            newPath = str(index) + ":" + split[1] 
            pathWriter.write(newPath) 

            print "[" + split[0] + "]" + split[1]
            index = index + 1

        newPath = str(index) + ":" + currPath
        pathWriter.write(newPath) 
    else:
        appendStr =  "0:" + os.getcwd() + "\n"
        pathWriter.write(appendStr)
elif len(arglist) == 2: 
    if  arglist[1] == "-h": #Get the top path from stack
        print "[pather.py -h ] Help" 
        print "[pather.py p  ] Top path" 
        print "[pather.py l  ] List all paths" 
        print "[pather.py -ra] Remov all paths" 
        print "[pather.py r 3] Remove index 3 from" 
        print "[pather.py 2  ] List index 3" 
    elif  arglist[1] == "p": #Get the top path from stack
        if len(plist) > 0: 
            topList = plist[len(plist)-1]
            split = re.split(":", topList)
            if len(split) > 1:
                sys.stdout.write(split[1])
            else:
                sys.stdout.write("Path ERROR: split=[", split, "]")

    elif arglist[1] == "l": #List all the path
        for item in plist:
            list = re.split(":", item)
            print "[" + str(list[0]) + "]" + list[1].rstrip()
            if len(list) > 1:
                index = list[0]
                path = os.getcwd()
                newIndex = int(index) + 1;
                appendStr = str(newIndex) + ":" + path + "\n"

    elif arglist[1].isdigit() : #Indexes path from stack
        pindex = int(arglist[1])
        if len(plist)-1 >= pindex:
            lineIndex = int(arglist[1]);

            index = 0
            for item in plist:
                if index == pindex:
                    list = re.split(":", item)
                    print list[1].rstrip()
                index = index + 1

    elif arglist[1] == "-ra": #Remove all the paths from stack
        pathWriter.seek(0)
        pathWriter.truncate()
            
elif len(arglist) == 3: 
    if  arglist[1] == "r" and arglist[2].isdigit(): #Delete index from stack
        plist.pop(int(arglist[2]))

        pathWriter.seek(0)
        pathWriter.truncate()

        index = 0
        for item in plist:
            list = re.split(":", item)
            pathWriter.write(str(index) + ":" + list[1])
            index = index + 1

    elif arglist[1] == "cd" and arglist[2].isdigit():
         dirIndex = int(arglist[2]) 
         mypath = plist[dirIndex][1]
         todir = mypath[:len(mypath)-1]
         print todir
         os.chdir(todir) 
pathWriter.close()


#Return to command line mode
