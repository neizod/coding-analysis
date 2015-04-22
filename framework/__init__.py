import argparse
import argcomplete

from ._utils import submodules


def run():
    parser = argparse.ArgumentParser(description='''
        This is master control file of the coding-analysis framework.''')
    main_subparsers = parser.add_subparsers()
    for module in submodules(__file__, __name__):
        module.update_parser(main_subparsers)
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if 'function' in args:
        args.function(**vars(args))
    else:
        parser.print_help()
