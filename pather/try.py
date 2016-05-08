#!/usr/bin/python
import re;
import os;
import sys;


pathfile    = "/Users/cat/myfile/github/python/pather/path.txt"
pathWriter  = open(pathfile, "r+")

listList = []
columnList = []
arglist = sys.argv;


print "cool"

def removeDuplicate(list, str):
    list = list[:];
    for line in list:
        splitList = re.split(':', line)
        if splitList[1] == str:
            list.remove(line)

        print splitList
        print line 

    return list 


listList = []

list =  []
list.append("1:cool")
listList.append(list);

list =  []
list.append("2:yes")
listList.append(list);

listList = removeDup(listList, "")
for item in listList:
    print item


