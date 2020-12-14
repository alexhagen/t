import argparse
import yaml
import os
import re
import sys
import subprocess
import itertools
import time
import numpy as np
import tqdm
import pync
import time
import urllib
from selenium import webdriver
import pickle

home = os.path.expanduser("~")


colors = itertools.cycle([
    '\033[95m',
    '\033[94m',
    '\033[96m',
    '\033[92m',
    '\033[93m',
    '\033[91m',
    '\033[1m',
    '\033[4m'])
colors = []
style = 7
for fg in range(31,38):
    #for bg in range(40,48):
    #    if (fg - 30) == (bg - 40):
    #        continue
    format = ';'.join([str(fg)])
    colors.append('\x1b[%sm' % (format))
colors = itertools.cycle(colors)
endcolor = '\033[0m'

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
        self.t_path = os.path.join(os.path.expanduser('~'), '.t')
        self.t_filename = os.path.join(self.t_path, 't')
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
                    color = next(colors)
                    print(f'{color}{project}{endcolor}')
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
        data = self._get_data()
        path = os.path.join(data['projects'][project]['path'])
        with open(os.path.join(path, '.todo'), 'a') as f:
            f.write(f"{task}\n")
        devnull = open(os.devnull, 'w')
        p = subprocess.Popen(['git', 'add', '.todo'],
                             cwd=path, stdout=devnull)
        p.wait()
        p = subprocess.Popen(['git', 'commit', '-m', f'adding task "{task}"'],
                             cwd=path, stdout=devnull)
        p.wait()
        devnull.close()

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
            i = 0
            color = next(colors)
            path = os.path.join(data['projects'][project]['path'])
            todo_filename = os.path.join(path, '.todo')
            if os.path.exists(todo_filename):
                f = open(todo_filename)
                for i, task in enumerate(f):
                    print(f'{color}#{i} [{project}]{endcolor}: {task.strip()}')
            if 'jira_boards' in data['projects'][project].keys():
                for jira_board in data['projects'][project]['jira_boards']:
                    xml_file = f'/tmp/{project}_jira.xml'
                    if os.path.isfile(xml_file):
                        xml = open(xml_file, 'r').read()
                    else:
                        url = jira_board
                        options = webdriver.ChromeOptions()
                        #options.add_argument("user-data-dir=/Users/hage581/Library/Application\ Support/Google/Chrome/Default/") #Path to your chrome profile
                        #options.add_experimental_option("detach", True)
                        driver = webdriver.Chrome(executable_path=rf"{home}/chromedriver", options=options)
                        driver.get('https://jira.pnnl.gov')
                        driver.find_element_by_name("os_username").send_keys(open(f'{home}/.username', 'r').read().strip())
                        driver.find_element_by_name("os_password").send_keys(open(f'{home}/.password', 'r').read().strip())
                        driver.find_element_by_name("login").click()
                        time.sleep(3)
                        pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
                        cookies = pickle.load(open("cookies.pkl", "rb"))
                        for cookie in cookies:
                            driver.add_cookie(cookie)
                        driver.get(url)
                        time.sleep(1.0)
                        xml = driver.execute_script('return document.getElementById("webkit-xml-viewer-source-xml").innerHTML')
                        with open(xml_file, 'w') as f:
                            f.write(xml)
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(xml)
                    for child in root:
                        for grandchild in child:
                            title = grandchild.find('.//title')
                            if title is not None:
                                i += 1
                                print(f'{color}#{i} [{project}]{endcolor}: {title.text.strip()}')



    def complete(self):
        parser = argparse.ArgumentParser(description='List all Tasks')
        parser.add_argument('project')
        parser.add_argument('taskno', type=int)
        args = parser.parse_args(sys.argv[2:])
        project = args.project
        taskno = args.taskno
        data = self._get_data()
        path = os.path.join(data['projects'][project]['path'])
        with open(os.path.join(path, '.todo'), "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i, _task in enumerate(d):
                if i != taskno:
                    f.write(_task)
                else:
                    task = _task
            f.truncate()
        devnull = open(os.devnull, 'w')
        p = subprocess.Popen(['git', 'add', '.todo'],
                             cwd=path, stdout=devnull)
        p.wait()
        p = subprocess.Popen(['git', 'commit', '-m', f'completed task "{task}"'],
                             cwd=path, stdout=devnull)
        p.wait()
        data = self._get_data()
        if 'completion_log' not in data.keys():
            data['completion_log'] = []
        data['completion_log'].append(dict(time=time.time(), project=project,
                                           taskno=taskno, task=task))
        self._write_data(data)
        p = subprocess.Popen(['git', 'commit', '-am', f'completed task "{task}"'],
                             cwd=self.t_path, stdout=devnull)
        p.wait()

    def focus(self):
        parser = argparse.ArgumentParser(description="Focus and log to a project")
        parser.add_argument('project')
        parser.add_argument('taskno', type=int)
        args = parser.parse_args(sys.argv[2:])
        project = args.project
        taskno = args.taskno
        data = self._get_data()
        path = os.path.join(data['projects'][project]['path'])
        with open(os.path.join(path, '.todo'), "r") as f:
            d = f.readlines()
            f.seek(0)
            for i, _task in enumerate(d):
                if i == taskno:
                    task = _task
        print(chr(27) + "[2J")
        print(f"Focusing on {task} for {project}.")
        for _ in tqdm.tqdm(np.arange(50), unit='min', unit_scale=0.5):
            time.sleep(30)
        pync.notify(f'Finished working for 25 minutes on {task} for {project}.  Take 5 minutes rest.', title='Finished Focus Session')
        if 'focus_sessions' not in data.keys():
            data['focus_sessions'] = []
        data['focus_sessions'].append(dict(timestamp=time.time(), task=task, project=project))
        self._write_data(data)

    def add_jira(self):
        parser = argparse.ArgumentParser(description="Add a jira board to a project")
        parser.add_argument('project')
        parser.add_argument('url')
        args = parser.parse_args(sys.argv[2:])
        project = args.project
        url = args.url
        data = self._get_data()
        if 'jira_boards' not in data['projects'][project].keys():
            data['projects'][project]['jira_boards'] = []
        data['projects'][project]['jira_boards'].append(url)
        self._write_data(data)

    def sync(self):
        # go through all todo lists and push, as well as the local push
        pass

    def c(self):
        self.complete()

    def a(self):
        self.add()

    def ls(self):
        self.list()

    def lsp(self):
        self.listproj()

if __name__ == "__main__":
    t()