#!/usr/bin/python3
from sys import argv

def main():
    for i in range(len(argv)):
        print(i,':',argv[i])

def get_help():
    h = 'usage: echoargs [ARGS [ARGS ...]]\n'
    h+='\nEchos args passed to it.\n'
    return h

if __name__ == "__main__":
    main()

