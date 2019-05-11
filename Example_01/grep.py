import os, sys
from werkzeug import exceptions


##Input Validation
if len(sys.argv) != 3:
    print("Usage: you should provide 2 arguments: 1) Needed Word   2)Path of the file to be scanned")
    exit(1)

if sys.argv[1] != "":
    word = sys.argv[1]
else:
    print("Usage: Please enter a valid word to be searched!")
    exit(2)

if  os.path.isfile(sys.argv[2]):
    path = sys.argv[2]
else:
    print("Usage: Please enter a valid file path to be used for scanning!")
    exit(4)

##Processing the file, and performing needed error handling
try:
    with open(path, 'r') as f:
        for line in f:
            if word in line:
                print(line)
except IOError as e:
    print("Internal file error occurred: %s", e)
    exit(5)
except:
    print("Unknown Error Occurred!")
    exit(6)
