#!/usr/bin/python
import re;
import os;
import sys;
import curses

stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
stdscr.addstr(0, 0, 'A cool stuff', curses.color_pair(1))
stdscr.refresh()


fileDir     = "/cygdrive/c/aronfile/github/pather"
configfile  = fileDir + "/config.txt"
pathfile    = fileDir + "/path.txt"
confWriter  = open(configfile, "w")
pathWriter  = open(pathfile, "r+")

listList = []
columnList = []
arglist = sys.argv;

for line in iter(pathWriter):
    splitList = re.split(':', line)
    listList.append(splitList)


# push path to stack
if len(arglist) == 1:
    newIndex = 0
    if  len(listList) > 0:
        for list in listList:
            if len(list) > 1:
                index = list[0]
                path = os.getcwd()
                newIndex = int(index) + 1;
                appendStr = str(newIndex) + ":" + path + "\n"
            else:
                print "error:", columnList
        pathWriter.write(appendStr)
    else:
        appendStr =  "0:" + os.getcwd() + "\n"
        pathWriter.write(appendStr)
elif len(arglist) == 2: 
    if  arglist[1] == "-h": #Get the top path from stack
        print "[pather.py -h ] Help" 
        print "[pather.py p  ] Top path" 
        print "[pather.py l  ]  List all paths" 
        print "[pather.py -ra] Remov all paths" 
        print "[pather.py r 3] Remove index 3 from stack" 
    elif  arglist[1] == "p": #Get the top path from stack
        if len(listList) > 0: 
            topList = listList[len(listList)-1]
            sys.stdout.write(topList[1])

    elif arglist[1] == "l": #List all the path
        axisY = 0
        axisX = 0
        for list in listList:
            if len(list) > 1:
                index = list[0]
                #sys.stdout.write(index + " : " + list[1])


                stdscr.addstr(axisX, 0, index + ":" + list[1], curses.color_pair(1))

                path = os.getcwd()
                newIndex = int(index) + 1;
                appendStr = str(newIndex) + ":" + path + "\n"
            else:
                print "error:", columnList
            axisX = axisX + 1

        stdscr.getkey()
    elif arglist[1].isdigit() : #Indexes path from stack
        if len(listList)-1 >= int(arglist[1]):
            lineIndex = int(arglist[1]);
            path = listList[lineIndex][1];
            sys.stdout.write(path)

    elif arglist[1] == "-ra": #Remove all the paths from stack
        pathWriter.close()
        open(pathfile, 'w').close()
            
elif len(arglist) == 3: 
    if  arglist[1] == "r" and arglist[2].isdigit(): #Delete index from stack
        listList.pop(int(arglist[2]))

        newlistList = []
        count = 0
        listlist = []
        for newlist in listList:
            newlist[0] = str(count) 
            newlist[1] = newlist[1]
            newlistList.append(newlist)
            count = count + 1

        pathWriter.close()
        open(pathfile, 'w').close()
        pathWriter  = open(pathfile, "r+")
        listList = newlistList[:]
        print listList
        for list in listList:
            print "list[0]=", list[0], "list[1]:", list[1]
            pathWriter.write(list[0] + ":" + list[1])
    elif arglist[1] == "cd" and arglist[2].isdigit():
         dirIndex = int(arglist[2]) 
         mypath = listList[dirIndex][1]
         todir = mypath[:len(mypath)-1]
         print todir
         os.chdir(todir) 
pathWriter.close()

#Return to command line mode
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
