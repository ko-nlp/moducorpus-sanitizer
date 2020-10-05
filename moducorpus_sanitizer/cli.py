import argparse
import os

from .about import __version__


def show_version(args):
    print(f'moducorpus_sanitizer=={__version__}')


def main():
    parser = argparse.ArgumentParser(description='moducorpus-sanitizer Command Line Interface')
    parser.set_defaults(func=show_version)
    subparsers = parser.add_subparsers(help='moducorpus_sanitizer')

    # version
    parser_version = subparsers.add_parser('version', help='Show version')

    # News
#     parser_news = subparsers.add_parser('version', help='Show version')
#     parser_news.add_argument('--input_dir', required=True, type=str, help='path/to/NIKL_NEWSPAPER(v1.0)')

    # Do task
    args = parser.parse_args()
    print('## Arguments of Moducorpus sanitizer ##')
    for name, var in sorted(vars(args).items()):
        if callable(var):
            print(f'  - {name} : {var.__name__}')
        else:
            print(f'  - {name} : {var}')
    task_function = args.func
    task_function(args)


if __name__ == '__main__':
    main()