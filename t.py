import argparse
import yaml
import os
import re
import sys
import subprocess

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
        self.t_filename = os.path.join(os.path.expanduser('~'), '.t')
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
        data = self._get_data()
        if data is not None:
            if 'projects' in data.keys():
                for project in data['projects'].keys():
                    print(project)
        else:
            print("t is not tracking any projects yet")

    def _get_data(self):
        data = yaml.load(open(self.t_filename), Loader=yaml.FullLoader)
        return data

    def _write_data(self, data):
        with open(self.t_filename, 'w') as f:
            yaml.dump(data, f)
        return

    def addproj(self):
        parser = argparse.ArgumentParser(description="Add a project to track")
        parser.add_argument('projectname')
        parser.add_argument('path')
        args = parser.parse_args(sys.argv[2:])
        projectname = args.projectname
        path = args.path
        # print the list of projects from the t yaml file
        data = self._get_data()
        if data is None:
            data = {'projects': {}}
        if 'projects' not in data.keys():
            data['projects'] = {}
        if projectname not in data['projects'].keys():
            data['projects'][projectname] = dict(path=os.path.abspath(path))
        self._write_data(data)
        print(f"added {projectname} to t!")

    def add(self):
        parser = argparse.ArgumentParser(description="Add a task to a project")
        parser.add_argument('project')
        parser.add_argument('task')
        args = parser.parse_args(sys.argv[2:])
        project = args.project
        task = args.task
        print(project, task)
        data = self._get_data()
        path = os.path.join(data['projects'][project]['path'])
        with open(os.path.join(path, '.todo'), 'a') as f:
            f.write(task)
        p = subprocess.Popen(['git', 'add', '.todo'],
                             cwd=path)
        p.wait()
        p = subprocess.Popen(['git', 'commit', '-m', f'adding task "{task}"'],
                             cwd=path)
        p.wait()

    def list(self):
        data = self._get_data()
        if len(sys.argv) > 2:
            parser = argparse.ArgumentParser(description='List all Tasks')
            parser.add_argument('project')
            args = parser.parse_args(sys.argv[2:])
            project = args.project
            projects = [project]
        else:
            projects = data['projects'].keys()
        for project in projects:
            path = os.path.join(data['projects'][project]['path'])
            f = open(os.path.join(path, '.todo'))
            for task in f:
                print(f'[{project}]: {task.strip()}')

if __name__ == "__main__":
    t()