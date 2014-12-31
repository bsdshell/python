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
# readCodeLine file.java l

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
    except IOError:
        print "Open file ["+fullPathFile+"] error"


readHandler.close()

