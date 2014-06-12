import errno
import shutil 
import ntpath 
import time
import sys;
import os;
# read file line by line to listList
def readfile(pathFileName):
    pathWriter  = open(pathFileName, "r+")
    listList = []
    for line in iter(pathWriter):
        line = line.strip(" \n\r\t")
        if(len(line) > 0):
            listList.append(line)
    pathWriter.close()
    return listList

# copy source directory to destination
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('directory not copied. Error: %s' % e)

# rename all index in the filename
def renameIndex(listList):
    newListList = []
    if len(listList) > 1:
        fileIndex = 0
        for line in listList:
            if len(line) > 0:
                basename = os.path.basename(line) 
                tokenList = basename.split('_')
                print(tokenList)

                llen = len(tokenList)
                if(llen > 0):
                    tokenList[llen-1] = str(fileIndex + 1)

                newfilename = ""
                for item in tokenList:
                    newfilename += item + "_" 
                    
                if(len(newfilename) > 0):
                    newfilename = newfilename.rstrip('_')
                print(newfilename)
                #line = line+"_"+str(len(listList)+1)
                print(line)
                finalPath = destinationPath + newfilename 
                newListList.append(finalPath)
                fileIndex = fileIndex + 1
    return newListList 

# max=1 index from filename e.g. myfile_2014_11_09_12_10_20_1
def getMaxIndex(listList):
    max = 0
    for line in listList:
        if len(line) > 0:
            basename = ntpath.basename(line) 
            tokenList = basename.split('_')
            print(tokenList)
            if(len(tokenList) > 0):
                index = int(tokenList[len(tokenList)-1])
                if(index > max):
                    max = index
    return max

# write all paths to file 
def writeListToFile(listList, sourcePath, pathFileName):
    # first file path
    pathWriter  = open(pathFileName, "w+")
    if len(listList) == 0:
        strftime = time.strftime("%Y_%d_%d_%H_%M_%S") + "_0"
        basename = ntpath.basename(sourcePath) + "_" + strftime
        finalPath= destinationPath + basename
        copy(sourcePath, finalPath)
        pathWriter.write(finalPath + '\n')
    else:
        strftime = time.strftime("%Y_%d_%d_%H_%M_%S_") + str(getMaxIndex(listList) + 1) 
        newbasename = ntpath.basename(sourcePath) + "_" + strftime
        finalPath = destinationPath + newbasename 
        copy(sourcePath, finalPath)
        listList.append(finalPath)

        for line in listList:
            pathWriter.write(line+'\n')
    pathWriter.close()

def listPath(pathFileName, listList):
    pathWriter  = open(pathFileName, "r+")
    index = 0
    for line in listList:
        print("["+str(index)+"]"+line)
        index = index + 1
    pathWriter.close()

def removeFileByIndex(pathFileName, listList):
    print(listList)
    print(arglist[2])
    print("pop=" + arglist[2])
    if(int(arglist[2]) < len(listList)):
        removepath = listList[int(arglist[2])]
        print(removepath)
        shutil.rmtree(removepath)

        listList.pop(int(arglist[2]))  
        pathWriter  = open(pathFileName, "w+")
        for line in listList:
            line = line.strip(" \n\r\t")
            pathWriter.write(line + "\n")
        pathWriter.close()

def copyRevisionToSource(revisionPath, sourcePath):
    shutil.copytree(revisionPath, sourcePath)

LIST = "l"
DELETE = "d"
REVERSE = "rev"
arglist = sys.argv;
pathFileName = './pathList.txt'
sourcePath = '/Users/cat/try/source'
destinationPath = '/Users/cat/try/backup/'
basename = ntpath.basename(sourcePath) + "_" + time.strftime("%Y_%d_%d_%H_%M_%S") 
finalPath= destinationPath + basename

listList = readfile(pathFileName) 

if len(arglist) == 1:
    writeListToFile(listList, sourcePath, pathFileName) 
if len(arglist) == 2 and arglist[1] == LIST:
    listPath(pathFileName, listList)    
elif len(arglist) == 3:
    if(arglist[1] == DELETE and arglist[2].isdigit()):
        removeFileByIndex(pathFileName, listList)
        listPath(pathFileName, listList)    
    elif(arglist[1] == REVERSE and arglist[2].isdigit()):
        writeListToFile(listList, sourcePath, pathFileName) 
        newListList = readfile(pathFileName)
        basename = os.path.basename(sourcePath) 
        hostPath = sourcePath.rstrip(basename)
        sourceFile = newListList[int(arglist[2])];
        print(sourcePath)
        print(hostPath)
        print(sourceFile)
        #baseName = 
        #print("sourcefile="+sourceFile)
        shutil.move(sourceFile, hostPath)
        shutil.rmtree(sourcePath)
        os.rename(hostPath+"/"+basename, sourcePath) 
