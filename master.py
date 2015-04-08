#!/usr/bin/env python3

import argparse
import argcomplete

from framework import codejam
from framework.codejam import get_metadata
from framework.codejam import get_source


def main():
    parser = argparse.ArgumentParser(description='''
        This is master control file of the coding-analysis framework.''')
    subparsers = parser.add_subparsers()

    codejam.get_metadata.update_parser(subparsers)
    codejam.get_source.update_parser(subparsers)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if 'function' in args:
        args.function(**vars(args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
