import argparse
import os

from .about import __version__
from .modu_news import news_to_corpus


def show_version(args):
    print(f'moducorpus_sanitizer=={__version__}')


def show_arguments(args):
    print('## Arguments of Moducorpus sanitizer ##')
    for name, var in sorted(vars(args).items()):
        if callable(var):
            print(f'  - {name} : {var.__name__}')
        else:
            print(f'  - {name} : {var}')


def main():
    parser = argparse.ArgumentParser(description='moducorpus-sanitizer Command Line Interface')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.set_defaults(func=show_version)
    subparsers = parser.add_subparsers(help='moducorpus_sanitizer')

    # version
    parser_version = subparsers.add_parser('version', help='Show version')

    # News
    parser_news = subparsers.add_parser('news', help='News corpus')
    parser_news.add_argument('--input_dir', required=True, type=str, help='path/to/NIKL_NEWSPAPER(v1.0)')
    parser_news.add_argument('--output_dir', required=True, type=str, help='path/to/corpus/NIKL_NEWSPAPER(v1.0)')
    parser_news.add_argument('--type', type=str, default='doublespaceline', choices=['multiline', 'doublespaceline'])
    parser_news.add_argument('--fields', type=str, nargs='+', default=['title', 'paragraph'], choices=['title', 'author', 'publisher', 'date', 'topic', 'original_topic', 'paragraph'])
    parser_news.set_defaults(func=news_to_corpus)

    # Do task
    args = parser.parse_args()
    show_arguments(args)
    task_function = args.func
    task_function(args)


if __name__ == '__main__':
    main()