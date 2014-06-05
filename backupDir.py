import errno
import shutil 
import ntpath 
import time

sourcePath = '/cygdrive/c/aronfile_old/ControlSerialize/WindowsFormsApplication2'
destinationPath = '/cygdrive/c/try/'

basename = ntpath.basename(sourcePath) + "_" + time.strftime("%Y_%d_%d_%H_%M_%S") 
finalPath= '/cygdrive/c/try/' + basename


print finalPath

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('directory not copied. Error: %s' % e)

copy(sourcePath, finalPath)
