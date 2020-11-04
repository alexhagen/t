import argparse

class Store(dict):
    def __init__(self):
        pass


## for finding things in a directory
import os
import re

def findfiles(path, regex):
    regObj = re.compile(regex)
    res = []
    for root, dirs, fnames in os.walk(path):
        for fname in fnames:
            if regObj.match(fname):
                res.append(os.path.join(root, fname))
    return res

print (findfiles('.', r'my?(reg|ex)'))
def grep(filepath, regex):
    regObj = re.compile(regex)
    res = []
    with open(filepath) as f:
        for line in f:
            if regObj.match(line):
                res.append(line)
    return res


if __name__ == "__main__":
    # parse args
    # run command
    pass