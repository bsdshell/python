import re;
import os;
import sys;
import subprocess

readHandler   = open('/tmp/text.txt')
fileDir = "/tmp/"
arglist = sys.argv;

count = 0
index0 = 0
index1 = 0
        
basename = os.path.basename("/dog/dog/dog.txt")
pair = os.path.splitext(basename)
newFileName = fileDir + pair[0] + ".html"
writeHandler  = open(newFileName, "w+")
currDir = os.getcwd();

print "currDir="+currDir
print "newFileName="+newFileName
print "basename="+basename
print "noextension="+pair[0]
print "index0="+str(index0)
print "index1="+str(index1)
for line in iter(readHandler):
        if len(arglist) == 2 and arglist[1] == "l":
            print "["+str(count)+"]"+line
        elif len(arglist) == 4:
            fileName = arglist[1]
            fullPath = currDir+"/"+fileName
            index0 = int(arglist[2])
            index1 = int(arglist[3])
            subprocess.call(["pygmentize"])

            print "fullPath="+fullPath
            print "[1]"+arglist[1]
            print "[2]"+arglist[2]
            print "[3]"+arglist[3]
        if (index0 <= count) and (count <= index1) :
            print "["+str(count)+line
            writeHandler.write(line);
        count = count+1
readHandler.close()
writeHandler.close()
