import re;
import os;
import sys;
import subprocess
import inspect

# python readCodeLine.py file.java  1   10
# List file line by line
# Syntax: readCodeLine file.java l

arglist = sys.argv;
currDir = os.getcwd()
index0 = 0
index1 = 0

print "currDir="+currDir 

def generate(sourceFile, destFile, index0, index1):
    pair = os.path.splitext(sourceFile)
    tmpFileName = currDir + "/" + pair[0] + "_tmp.java"

    sourceFullFile = currDir + "/" + sourceFile
    destFullFile   = currDir + "/" + destFile

    tmpWriteHandler = open(tmpFileName, "w+")
    readHandler = open(sourceFullFile, "r")
    count = 0
    for line in iter(readHandler):
        if (index0 <= count) and (count <= index1) :
            print "[" + str(count) +"]" + line.rstrip("\n")
            tmpWriteHandler.write(line)
        count = count + 1

    tmpWriteHandler.close()
    readHandler.close()

    htmlFile = destFullFile 
    subprocess.call(["pygmentize", "-f", "html", "-o", htmlFile, tmpFileName])


if len(arglist) == 1:
    print "[0] readCodeLine file.java l   [list line #]"
    print "[1] readCodeLine file.java 1 20 [ Color line 1 to 20, file.html is generated]"
elif len(arglist) == 3 and arglist[2] == "l":
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
elif len(arglist) == 4 and arglist[2].isdigit() and arglist[3].isdigit():
    # etc. file.java
    fileName = arglist[1] 
    pair = os.path.splitext(fileName)
    print currDir
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

    basename = os.path.basename(fileName)
    htmlPair = os.path.splitext(basename)

    htmlFile = currDir + "/" + htmlPair[0] + ".html"
    subprocess.call(["pygmentize", "-f", "html", "-o", htmlFile, tmpFileName])

elif len(arglist) == 5 and arglist[3].isdigit() and arglist[4].isdigit():
    sourceFile = arglist[1]
    destFile = arglist[2]
    index0 = int(arglist[3])
    index1 = int(arglist[4])
    generate(sourceFile, destFile, index0, index1)
