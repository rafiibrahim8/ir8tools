#!/usr/bin/python3
from datetime import datetime
from subprocess import run
import os
import argparse

VERSION = 1.0

def to_git(message=None):
    if(not os.path.exists('.git/config')):
        print('Can not find git repository on this location:',os.getcwd())
        return
    
    try:
        run('git add --all'.split())
    except:
        print('git is not installed. Please install git and try again.')
        return
    
    if(not message):
        message = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    command = 'git commit -m'.split()
    command.append(message)
    
    run(command)
    run('git push -u origin HEAD'.split())

def main():
    parser = argparse.ArgumentParser(description='One command commit and push to current git branch.',add_help=False)
    parser.add_argument(type=str,dest='msg',nargs='*',metavar='MESSAGE',help='Add commit message. Current date and time will be added as message if this parameter is missing.')
    parser.add_argument('-v','--version',help='Prints version information.',action='version',version= 'v'+str(VERSION))
    parser.add_argument('-h','--help', help='Show this help message and exit.',action='help')
    args = parser.parse_args()
    to_git(' '.join(args.msg))


if __name__ == "__main__":
    main()
