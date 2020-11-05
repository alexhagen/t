import argparse
import yaml
import os
import re
import sys

class Store(dict):
    def __init__(self):
        pass


## for finding things in a directory


def findfiles(path, regex):
    regObj = re.compile(regex)
    res = []
    for root, dirs, fnames in os.walk(path):
        for fname in fnames:
            if regObj.match(fname):
                res.append(os.path.join(root, fname))
    return res

#print (findfiles('.', r'my?(reg|ex)'))
def grep(filepath, regex):
    regObj = re.compile(regex)
    res = []
    with open(filepath) as f:
        for line in f:
            if regObj.match(line):
                res.append(line)
    return res
    
class t(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='todo list',
                                         usage='t <command> [<args>]')
        parser.add_argument('command', help='subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('unrecognized command')
            parser.print_help()
            sys.exit(1)
        getattr(self, args.command)()

    def listproj(self):
        # load ~/.t
        t_filename = os.path.join(os.path.expanduser('~'), '.t')
        # print the list of projects from the t yaml file
        with open(t_filename) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if data is not None:
                if 'projects' in data.keys():
                    for project in data['projects']:
                        print(project)
            else:
                print("t is not tracking any projects yet")

    def addproj(self):
        parser = argparse.ArgumentParser(description="Add a project to track")
        parser.add_argument('project')
        args = parser.parse_args(sys.argv[2:])
        project = args.project
        # load ~/.t
        t_filename = os.path.join(os.path.expanduser('~'), '.t')
        # print the list of projects from the t yaml file
        data = yaml.load(open(t_filename), Loader=yaml.FullLoader)
        if data is None:
            data = {'projects': []}
        if 'projects' not in data.keys():
            data['projects'] = []
        if project not in data['projects']:
            data['projects'].append(os.path.abspath(project))
        with open(t_filename, 'w') as f:
            yaml.dump(data, f)
        print(f"added {project} to t!")


if __name__ == "__main__":
    t()