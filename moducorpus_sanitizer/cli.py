import argparse
import os

from .about import __version__
from .modu_mp import mp_to_corpus
from .modu_news import news_to_corpus


def show_version(args):
    print(f"moducorpus_sanitizer=={__version__}")


def show_arguments(args):
    print("## Arguments of Moducorpus sanitizer ##")
    for name, var in sorted(vars(args).items()):
        if callable(var):
            print(f"  - {name} : {var.__name__}")
        else:
            print(f"  - {name} : {var}")


def main():
    parser = argparse.ArgumentParser(
        description="moducorpus-sanitizer Command Line Interface"
    )
    parser.set_defaults(func=show_version)
    subparsers = parser.add_subparsers(help="moducorpus_sanitizer")

    # version
    parser_version = subparsers.add_parser("version", help="Show version")

    # News
    parser_news = subparsers.add_parser("news", help="News corpus")
    parser_news.add_argument("-i", "--input_dir", required=True, type=str, help="path/to/NIKL_NEWSPAPER")
    parser_news.add_argument("-o", "--output_dir", required=True, type=str, help="path/to/corpus/NIKL_NEWSPAPER")
    parser_news.add_argument("-t", "--type", type=str, default="doublespaceline", choices=["multiline", "doublespaceline"])
    parser_news.add_argument("--fields", type=str, nargs="+", default=["title", "paragraph"], choices=["title", "paragraph"])
    parser_news.set_defaults(func=news_to_corpus)

    # Morpheme
    parser_mp = subparsers.add_parser("mp", help="Morphological analysis corpus")
    parser_mp.add_argument("-i", "--input_dir", required=True, type=str, help="path/to/NIKL_MP")
    parser_mp.add_argument("-o", "--output_dir", required=True, type=str, help="path/to/corpus/")
    parser_mp.add_argument("-t", "--type", default="eojeol", type=str, help="output type")
    parser_mp.set_defaults(func=mp_to_corpus)

    # Do task
    args = parser.parse_args()
    show_arguments(args)
    task_function = args.func
    task_function(args)


if __name__ == "__main__":
    main()
