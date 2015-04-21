#!/usr/bin/env python3

import argparse
import argcomplete

from framework import download
from framework import prepare


def main():
    parser = argparse.ArgumentParser(description='''
        This is master control file of the coding-analysis framework.''')
    main_subparsers = parser.add_subparsers()
    for module in [download, prepare]:
        module.update_parser(main_subparsers)
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if 'function' in args:
        args.function(**vars(args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
