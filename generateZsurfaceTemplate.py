import re;
import os;
import sys;
import subprocess
import inspect

#The python script generates colour hightlighting code from source code files
#Use pygmentize to color source code in many programming languages

OPEN_MARKER  = '\/\/\['    # //[
CLOSE_MARKER = '\/\/\]'   # //]
FILE         = 'file'
TITLE        = 'title'

FILE_JAVA     = "java"
FILE_CPP      = "cpp"
FILE_HASKELL = "haskell"
FILE_SCALA    = "scala"
FILE_XCODE    = "xcode"

arglist   = sys.argv;
currDir   = os.getcwd()
colorPath = "/Library/WebServer/Documents/zsurface/colorhtml/"
index0 = 0
index1 = 0

print "currDir="+currDir 

# find the open marker and close marker
# open marker = '//['
# close marker = '//]'
def findColorCode(line, count, stack):
    openMarker = re.search(r'\/\/\[', line)
    closeMarker = re.search(r'\/\/\]', line)
    if openMarker:
        print 'openMarker:' ,  line  , "group:", openMarker.group()

        regex = re.compile(r'(file\W*=\W*)(\S+)\W*(title\W*=\W*)"(.*)"')
        match = regex.search(line)
        if match:
            print "(0)=", match.group(0)
            print "(1)=", match.group(1)
            print "(2)=", match.group(2)
            print "(3)=", match.group(3)
            print "(4)=", match.group(4)
        stack.append(OPEN_MARKER)
    elif closeMarker:
        print 'closeMarker:', line, " group:", closeMarker.group()
        if stack[0] == OPEN_MARKER: # balance //[ and //]
            print 'balance //[ and //]'
        else:
            print "Error: open and close markers are not balanced" 
        stack = []

def printmenu():
    print "[0] generateZsurfaceTemplate file.java                      [List file.java with line #]"
    print "[1] generateZsurfaceTemplate file.java 2 20                 [Color line from 2 to 20, file.html is generated in current directory]"
    print "[2] generateZsurfaceTemplate file.java color.html 2 20      [Color line from 2 to 20, color.html is generated in current directory]"
    print "[3] generateZsurfaceTemplate file.java color.html -d 2 20   [Color line from 2 to 20, color.html is generated in /Library/WebServer/Documents/zsurface/colorhtml/]"

def generate(sourceFile, htmlFile, index0, index1):
    basename = os.path.basename(sourceFile)
    pair = os.path.splitext(basename)
    #tmpFileName = currDir + "/" + pair[0] + "_tmp.java"
    tmpFileName = "/tmp/" + pair[0] + "_tmp" + pair[1]
    print "--tmpFileName="+tmpFileName
    print "--sourceFile="+sourceFile

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
    os.remove(tmpFileName)

if len(arglist) == 1:
    printmenu()
elif len(arglist) == 2:
    fullPathName = os.path.join(currDir, arglist[1]);
    if os.path.isfile(fullPathName):
        print "--fullPathName="+fullPathName
        try:
            readHandler = open(fullPathName, "r")
            count = 0
            stack = []
            for line in iter(readHandler):
                findColorCode(line, count, stack)            

                print "["+str(count)+"]"+line.rstrip("\n")
                count = count + 1

            readHandler.close()
        except IOError:
            print "--Open file ["+fullPathName+"] error"
    else:
        print "--Error: file["+fileName+"] does't exist"


# Syntax highlight from line 1 to 10 
# Syntax: generateZsurfaceTemplate.py source.java 1 10
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
    print "--sourceFile="+sourceFile
    print "--htmlFile="+htmlFile



# Syntax: readCodeLine source.java diffFile.html -d 1 10
elif len(arglist) == 6 and arglist[3] == "-d" and arglist[4].isdigit() and arglist[5].isdigit():
    sourceFile = arglist[1]
    pair = os.path.splitext(sourceFile) 
    
    fullPath = "." 
    if pair[1] == ".java":
        fullPath = os.path.join(colorPath, FILE_JAVA)
    elif pair[1] == ".cpp":
        fullPath = os.path.join(colorPath, FILE_CPP)
    elif pair[1] == ".hs":
        fullPath = os.path.join(colorPath, FILE_HASKELL)
    elif pair[1] == ".m":
        fullPath = os.path.join(colorPath, FILE_XCODE)
    elif pair[1] == ".scl":
        fullPath = os.path.join(colorPath, FILE_SCALA)

    if os.path.exists(fullPath):
        print "--fullPath="+fullPath
        htmlFile = os.path.join(fullPath, arglist[2]);
        lineStart= int(arglist[4])
        lineEnd= int(arglist[5])
        generate(sourceFile, htmlFile, lineStart, lineEnd)
        print "--fullPath="+fullPath
        print "--sourceFile="+sourceFile
        print "--htmlFile="+htmlFile
    else: 
        print "--Error: path=["+fullPath+"] does't exist"
