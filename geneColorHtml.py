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

HTML_BEG      = "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en-GB\"> <head> <link rel=\"stylesheet\" type=\"text/css\" href=\"mycss/style.css\" /> </head><body>" 
HTML_END      = "</body> </html>" 

STAR           = r'\*.*\*'
SQUARE_BRACKET = r'\[.*\]'
CURE_BRACKET   = r'{.*}'
CURE_ANGLE     = r'<.*>'
DOUBLE_SLASH         = r'\/\/.*'

arglist   = sys.argv;
currDir   = os.getcwd()
colorPath = "/Library/WebServer/Documents/zsurface/colorhtml/"
index0 = 0
index1 = 0

print "currDir="+currDir 

def printList(mylist):
    for li in mylist:  
        print li

def readFileLineByLine(sourceFile):
    readHandler = open(sourceFile, "r")
    flist = []
    for line in iter(readHandler):
        flist.append(line)

    readHandler.close()

    return flist

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
        
def geneNoteHtml(inFile, outFile):
    end = "<br>"
    newline = "\n"
    span_open = "<span class=\"tit\">"
    span_close = "</span>"

    span_open_ = "<span>"
    span_close_ = "</span>"


    flist = readFileLineByLine(inFile)
    tmpWriteHandler = open(outFile, "w+")
    tmpWriteHandler.write(HTML_BEG + end)
    for line in flist:
        nline = line = line.strip()
        re0 = re.compile(STAR)
        re1 = re.compile(SQUARE_BRACKET)
        re2 = re.compile(CURE_BRACKET)
        re3 = re.compile(CURE_BRACKET)
        re4 = re.compile(CURE_ANGLE)
        re5 = re.compile(DOUBLE_SLASH)

        match0 = re0.search(line)
        match1 = re1.search(line)
        match2 = re2.search(line)
        match3 = re3.search(line)
        match4 = re4.search(line)
        match5 = re5.search(line)

        print "line=" + line
        if len(line) > 0:
            if match0:
                if line[0] == '*' and line[-1] == '*':
                    nline = span_open + line[1:len(line)-1] +span_close 
            elif match1:
                if line[0] == '[' and line[-1] == ']':
                    nline = span_open + line[1:len(line)-1] + span_close
            elif match2:
                if line[0] == '{' and line[-1] == '}':
                    nline = span_open + line[1:len(line)-1] + span_close
            elif match3:
                if line[0] == '<' and line[-1] == '>':
                    nline = span_open + line[1:len(line)-1] + span_close
            elif match4:
                if line[0] == '<' and line[-1] == '>':
                    nline = span_open + line[1:len(line)-1] + span_close
            elif match5:
                if line[0] == '/' and line[1] == '/':
                    nline = span_open + line[2:len(line)-1] + span_close
            else:
                nline = span_open_  + line + span_close_ 

        else:
            nline = end 

        tmpWriteHandler.write(nline + end + newline)

        print nline 
    tmpWriteHandler.write(HTML_END+ end)
    tmpWriteHandler.close()

def iterateFile(sourceFile):
    readHandler = open(sourceFile, "r")
    count = 0
    list1 = {}
    foundOpenMarker = False;
    blockCode = ""

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
                stack.append(OPEN_MARKER)
                foundOpenMarker = True
                print "(0)=", match.group(0)
                print "(1)=", match.group(1)
                fNameHtml = match.group(2)

                print "(2)=file=", match.group(2)
                print "(3)=", match.group(3)
                titleHtml = match.group(4)
                print "(4)=title=", match.group(4)
                list1 = {'OPEN_MARKER': OPEN_MARKER, 'file':fNameHtml, 'title':titleHtml,'begin':count}

        elif closeMarker:

            openM = stack.pop()
            foundOpenMarker = False
            list1['end'] = count
            if len(blockCode) > 0 and openM == OPEN_MARKER:
                    pair = os.path.splitext(sourceFile)
                    lexer = get_lexer_by_name("java", stripall=True)

                    htmlFilePath = os.path.join(colorPath, FILE_JAVA, list1['file']);
                    if pair[1] == ".m":
                        lexer = get_lexer_by_name("objc", stripall=True)
                        htmlFilePath = os.path.join(colorPath, FILE_XCODE, list1['file']);
                    elif pair[1] == ".hs":
                        lexer = get_lexer_by_name("haskell", stripall=True)
                        htmlFilePath = os.path.join(colorPath, FILE_HASKELL, list1['file']);
                    elif pair[1] == ".cpp":
                        lexer = get_lexer_by_name("cpp", stripall=True)
                        htmlFilePath = os.path.join(colorPath, FILE_CPP, list1['file']);
                    elif pair[1] == ".scala":
                        lexer = get_lexer_by_name("scala", stripall=True)
                        htmlFilePath = os.path.join(colorPath, FILE_SCALA, list1['file']);

                    #formatter = HtmlFormatter(linenos=False, cssclass="source")
                    formatter = HtmlFormatter(linenos=False)

                    if os.path.exists(htmlFilePath):
                        print "Error: htmlFilePath=[", htmlFilePath, "] exist\n"
                        var = raw_input("Input 'rm' to remove the file\n")
                        if( var == "rm"):
                            os.remove(htmlFilePath)
                            print "Remove file=[", htmlFilePath, "]\n"
                        elif var == "": 
                            print "Skip generate:", htmlFilePath, "\n"
                    else:
                        htmlFileHandle = open(htmlFilePath, "w+")

                        highlight(blockCode, lexer, HtmlFormatter(), htmlFileHandle)

                        # reset blockCode and list1
                        list1 = {}

                    blockCode = ""    
        else:
            #if foundOpenMarker:
            if len(stack) == 1:
                blockCode += line 
                print "blockCode->", blockCode

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


# program start

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

elif len(arglist) == 4 and arglist[1] == "-h":
    printList(arglist)

    inFile = arglist[2]
    outFile = arglist[3]

    geneNoteHtml(inFile, outFile)
        

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
    elif pair[1] == ".scala":
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
