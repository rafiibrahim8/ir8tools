from ir8tools import __version__
from subprocess import run
from .echoargs import get_help as echoparams_help
from .tool_descriptions import print_tool_list
import argparse

def main():
    parser = argparse.ArgumentParser(description='A collection of scripts/tools', add_help=False)
    parser.add_argument('-l','--list',dest='toollist',action='store_true',help='Show the list of tools.')
    parser.add_argument('tool',nargs='*',metavar='TOOL',help='Name of the tool you want to run.',default=[])
    parser.add_argument('arg',nargs='*',metavar='ARGS',help='Arguments of the tool')
    parser.add_argument('-h','--help',dest='help',help='Show help for perticular tool or this message if no tool was given.',action='store_true')
    parser.add_argument('-v','--version',help='Prints version information.',action='version',version= 'v'+ str(__version__))
    
    parser.usage = parser.prog + ' [-h] [-v] [TOOL] [ARGS [ARGS ...]]'

    args = parser.parse_args()
    if(args.toollist):
        print_tool_list()
        return
    
    if(not args.tool):
        parser.print_help()
        return

    if(args.help and 'echoargs' == args.tool[-1]): # echoargs does not use argparse so printing help for it.
        print(echoparams_help())
        return
    
    if(args.help):
        args.tool.append('--help')
    
    run(args.tool)

if __name__ == "__main__":
    print('Method calls from this script only.')
    #main()
