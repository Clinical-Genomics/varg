"""
varg.__main__
The main entry point for the command line interface.
Invoke as ``varg`` (if installed)
or ``python -m varg`` (no install required).
"""
import sys

from varg.cli.root import root_command


def main():
    sys.exit(root_command())


if __name__ == "__main__":
    main()
