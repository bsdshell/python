from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re;
import os;
import sys;
import subprocess
import inspect


NAME= 'dog'
NAME1= "dog" 
mylist = [NAME, NAME1]
print mylist[0]
print mylist[1]

list1 = {}
def fun(list1):
    list1 = {'1':1, 'cat':3};
    return list1

mylist = {}
myl = fun(mylist)

print "--------------------------"
myl['suck'] = 'suck'

for s in myl:
    print "->", s

tmpWriteHandler = open("/tmp/file1.html", "w+")
code = 'print "Hello World"'
print highlight(code, PythonLexer(), HtmlFormatter(), tmpWriteHandler)

fileName ="/home/dog/cat.html" 
basename = os.path.basename(fileName)
pair = os.path.splitext(fileName)
print 'pair[0]=', pair[0]
print 'pair[1]=', pair[1]

