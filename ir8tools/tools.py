from ir8tools import __version__
from importlib import import_module
from .completions import SHELLS, get_script as completion_script
from .echoargs import get_help as echoargs_help
from .tool_descriptions import all_tools, print_tool_list
import argparse
import sys


def get_entry_point(name):
    """Return the main() function for the tool with the given name, or None."""
    for tool_name, _, link in all_tools[1:]:
        if tool_name == name:
            module, func = link.split("=", 1)[1].split(":")
            return getattr(import_module(module), func)
    return None


def main():
    parser = argparse.ArgumentParser(
        description="A collection of scripts/tools",
        epilog=(
            "fish completion:\n"
            "  ir8t --completions fish > ~/.config/fish/conf.d/ir8tools.fish"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )
    parser.add_argument(
        "-l",
        "--list",
        dest="toollist",
        action="store_true",
        help="Show the list of tools.",
    )
    parser.add_argument(
        "-h",
        "--help",
        dest="help",
        help="Show help for perticular tool or this message if no tool was given.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Prints version information.",
        action="version",
        version="v" + str(__version__),
    )
    parser.add_argument(
        "--completions",
        metavar="SHELL",
        choices=SHELLS,
        help="Print the completion script for SHELL ({}).".format(", ".join(SHELLS)),
    )
    parser.add_argument(
        "tool", nargs="?", metavar="TOOL", help="Name of the tool you want to run."
    )
    # Everything after the tool name belongs to the tool, flags included.
    parser.add_argument(
        "args", nargs=argparse.REMAINDER, metavar="ARGS", help="Arguments of the tool"
    )

    parser.usage = (
        parser.prog + " [-h] [-l] [-v] [--completions SHELL] [TOOL] [ARGS ...]"
    )

    args = parser.parse_args()
    if args.completions:
        sys.stdout.write(completion_script(args.completions))
        return

    if args.toollist:
        print_tool_list()
        return

    if not args.tool:
        parser.print_help()
        return

    entry_point = get_entry_point(args.tool)
    if entry_point is None:
        parser.error(
            "unknown tool '{}' (use --list to see available tools)".format(args.tool)
        )

    tool_args = args.args
    if args.help:
        if args.tool == "echoargs":  # echoargs does not use argparse.
            print(echoargs_help())
            return
        tool_args = ["--help"]

    # Run the tool in-process so it works even if its script isn't on PATH,
    # and so its exit status becomes ours.
    sys.argv[:] = [args.tool] + tool_args  # in place: echoargs holds a reference
    sys.exit(entry_point())


if __name__ == "__main__":
    print("Method calls from this script only.")
    # main()
