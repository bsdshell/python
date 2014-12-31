import re;
import os;
import sys;
import subprocess


# python readCodeLine.py file.java  1   10

arglist = sys.argv;

index0 = 0
index1 = 0
        
currDir = os.getcwd()

# List file line by line
# Syntax: readCodeLine file.java l

if len(arglist) == 3 and arglist[2] == "l":
    fileName = arglist[1]
    fullPathFile = currDir + "/" + fileName;
    print "fullPathFile="+fullPathFile
    try:
        readHandler = open(fullPathFile, "r")
        count = 0
        for line in iter(readHandler):
            print "["+str(count)+"]"+line.rstrip("\n")
            count = count + 1

        readHandler.close()
    except IOError:
        print "Open file ["+fullPathFile+"] error"


# Colour line from 1 to 10
# Syntax: readCodeLine file.java 1 10
if len(arglist) == 4 and arglist[2].isdigit() and arglist[3].isdigit():
    # etc. file.java
    fileName = arglist[1] 
    pair = os.path.splitext(fileName)
    tmpFileName = currDir + "/" + pair[0] + "_tmp.java"
    fullPathFile = currDir + "/" + fileName;
    tmpWriteHandler = open(tmpFileName, "w+")
    readHandler = open(fullPathFile, "r")
    index0 = int(arglist[2])
    index1 = int(arglist[3])
    count = 0
    for line in iter(readHandler):
        if (index0 <= count) and (count <= index1) :
            print "[" + str(count) +"]" + line.rstrip("\n")
            tmpWriteHandler.write(line)
        count = count + 1

    tmpWriteHandler.close()
    readHandler.close()
