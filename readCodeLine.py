import re;
import os;
import sys;
import subprocess
import inspect

#The python script generates colour hightlighting code from source code files
#Use pygmentize to color source code in many programming languages

arglist = sys.argv;
currDir = os.getcwd()
index0 = 0
index1 = 0

print "currDir="+currDir 

def generate(sourceFile, htmlFile, index0, index1):
    basename = os.path.basename(sourceFile)
    pair = os.path.splitext(basename)
    tmpFileName = currDir + "/" + pair[0] + "_tmp.java"
    print "tmpFileName="+tmpFileName
    print "sourceFile="+sourceFile


    tmpWriteHandler = open(tmpFileName, "w+")
    readHandler = open(sourceFile, "r")
    count = 0
    for line in iter(readHandler):
        if (index0 <= count) and (count <= index1) :
            print "[" + str(count) +"]" + line.rstrip("\n")
            tmpWriteHandler.write(line)
        count = count + 1

    tmpWriteHandler.close()
    readHandler.close()
    subprocess.call(["pygmentize", "-f", "html", "-o", htmlFile, tmpFileName])

if len(arglist) == 1:
    print "[0] readCodeLine file.java -l                    [List file.java with line #]"
    print "[1] readCodeLine file.java 2 20                  [Color line from 2 to 20, file.html is generated in current directory]"
    print "[2] readCodeLine file.java diffFile.html 2 20    [Color line from 2 to 20, diffFile.html is generated in current directory]"
elif len(arglist) == 3 and arglist[2] == "-l":
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
# Syntax: readCodeLine source.java 1 10
elif len(arglist) == 4 and arglist[2].isdigit() and arglist[3].isdigit():
    # etc. file.java
    basename = os.path.basename(arglist[1])
    sourceFile = currDir + "/" + basename 
    fileExt = os.path.splitext(basename)

    htmlFile = currDir + "/" + fileExt[0] + ".html"
    print "htmlfile="+htmlFile
    lineStart= int(arglist[2])
    lineEnd= int(arglist[3])

    generate(sourceFile, htmlFile, lineStart, lineEnd)

# Colour line from 1 to 10
# Syntax: readCodeLine source.java diffFile.html 1 10
elif len(arglist) == 5 and arglist[3].isdigit() and arglist[4].isdigit():
    sourceFile = arglist[1]
    htmlFile = arglist[2]
    lineStart= int(arglist[3])
    lineEnd= int(arglist[4])
    generate(sourceFile, htmlFile, lineStart, lineEnd)
