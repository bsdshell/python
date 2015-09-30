from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

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

OPEN_REG = 'OPEN_REG'
CLOSE_REG = 'CLOSE_REG'

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

def getMakerFromFileType(sourceFile):
    list1 = {};

    openReg  = re.compile(r'\/\/\[')
    closeReg = re.compile(r'\/\/\]')

    pair = os.path.splitext(sourceFile)
    if pair[1] == ".hs":
        openReg  = re.compile(r'--\[')
        closeReg = re.compile(r'--\]')
    elif pair[1] == ".py":
         openReg  = re.compile(r'##\[')
         closeReg = re.compile(r'##\]')
    list1 = { OPEN_REG:openReg, CLOSE_REG:closeReg};
    return list1

def geneColorHtml(list1):
    print "code for generate highlighting html"
    for s in list1:
        print "list->", s, " ", list1[s] 
        
def iterateFile(sourceFile):
    readHandler = open(sourceFile, "r")
    count = 0
    list1 = {}
    begBool = False;
    codeStr = ""

    mlist = getMakerFromFileType(sourceFile)
    openReg = mlist['OPEN_REG']
    closeReg= mlist['CLOSE_REG']

    regex = re.compile(r'(file\W*=\W*)(\S+)\W*(title\W*=\W*)"(.*)"')
    stack = []
    for line in iter(readHandler):
        openMarker = openReg.search(line)
        closeMarker = closeReg.search(line)    
        if openMarker:
            print 'openMarker:', line, "group:", openMarker.group()
            match = regex.search(line)
            if match:
                begBool = True
                print "(0)=", match.group(0)
                print "(1)=", match.group(1)
                fNameHtml = match.group(2)

                print "(2)=file=", match.group(2)
                print "(3)=", match.group(3)
                titleHtml = match.group(4)
                print "(4)=title=", match.group(4)
                list1 = {'OPEN_MARKER': OPEN_MARKER, 'file':fNameHtml, 'title':titleHtml,'begin':count}

        elif closeMarker:
            begBool = False
            list1['end'] = count
            if len(codeStr) > 0:
                    pair = os.path.splitext(sourceFile)
                    lexer = get_lexer_by_name("java", stripall=True)

                    htmlFilePath = os.path.join(colorPath, "java", list1['file']);
                    if pair[1] == ".m":
                        lexer = get_lexer_by_name("objc", stripall=True)
                        htmlFilePath = os.path.join(colorPath, "xcode", list1['file']);
                    elif pair[1] == ".hs":
                        lexer = get_lexer_by_name("haskell", stripall=True)
                        htmlFilePath = os.path.join(colorPath, "haskell", list1['file']);
                    elif pair[1] == ".cpp":
                        lexer = get_lexer_by_name("cpp", stripall=True)
                        htmlFilePath = os.path.join(colorPath, "cpp", list1['file']);
                    
                    #formatter = HtmlFormatter(linenos=False, cssclass="source")
                    formatter = HtmlFormatter(linenos=False)

                    if os.path.exists(htmlFilePath):
                        print "Error: htmlFilePath=", htmlFilePath, " exist"
                        sys.exit()
                    else:
                        htmlFileHandle = open(htmlFilePath, "w+")

                        highlight(codeStr, lexer, HtmlFormatter(), htmlFileHandle)

                        # reset codeStr and list1
                        codeStr = ""
                        list1 = {}
        else:
            if begBool:
                codeStr += line 
                print "codeStr->", codeStr


        print "["+str(count)+"]"+line.rstrip("\n")
        count = count + 1

def printmenu():
    print "[0] geneColorHtml file.java                      [List file.java with line #]"
    print "[1] geneColorHtml file.java 2 20                 [Color line from 2 to 20, file.html is generated in current directory]"
    print "[2] geneColorHtml file.java color.html 2 20      [Color line from 2 to 20, color.html is generated in current directory]"
    print "[3] geneColorHtml file.java color.html -d 2 20   [Color line from 2 to 20, color.html is generated in /Library/WebServer/Documents/zsurface/colorhtml/]"

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

def generate2(list1, readHandler):
    begIndex = list1['begin'];
    endIndex = list1['end'];
    fileName = list1['file'];
    htmlHandler = open("/tmp/" + fileName, "w+")
    count = 0
    codeStr = ""
    for line in iter(readHandler):
        if (begIndex <= count) and (count <= endIndex) :
            codeStr += line
            print "[" + str(count) +"]" + line.rstrip("\n")
        count = count + 1

    highlight(codeStr, PythonLexer(), HtmlFormatter(), htmlHandler)
    htmlHandler.close()

if len(arglist) == 1:
    printmenu()
elif len(arglist) == 2:
    sourceFile = os.path.join(currDir, arglist[1]);
    iterateFile(sourceFile)


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
