import argparse

from .about import __version__
from .modu_messenger import messenger_to_corpus
from .modu_newspaper import news_to_corpus
from .modu_spoken import spoken_to_corpus
from .modu_newspaper import AVAILABLE_FIELDS as NEWS_AVAILABLE_FIELDS
from .modu_spoken import AVAILABLE_FIELDS as SPOKEN_AVAILABLE_FIELDS


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
    parser = argparse.ArgumentParser(description="moducorpus-sanitizer Command Line Interface")
    parser.set_defaults(func=show_version)
    subparsers = parser.add_subparsers(help="moducorpus_sanitizer")

    commons = argparse.ArgumentParser(add_help=False)
    commons.add_argument("-i", "--input_dir", required=True, type=str, help="path/to/raw_corpus")
    commons.add_argument("-o", "--output_dir", required=True, type=str, help="path/to/sanitized_corpus/")
    commons.add_argument("--debug", dest="debug", action="store_true")
    commons.add_argument("--text_only", dest="text_only", action="store_true")
    commons.add_argument("--supress_error", dest="supress_error", action="store_true")

    # version
    p_version = subparsers.add_parser("version", help="Show version")
    p_version.set_defaults(func=show_version)

    # News
    p_news = subparsers.add_parser("news", parents=[commons], help="News corpus")
    p_news.add_argument("--fields", type=str, nargs="+", default=["title", "paragraph"], choices=NEWS_AVAILABLE_FIELDS)
    p_news.set_defaults(func=news_to_corpus)

    # Messenger
    p_messenger = subparsers.add_parser("messenger", parents=[commons], help="Messenger corpus")
    p_messenger.set_defaults(func=messenger_to_corpus)

    p_spoken = subparsers.add_parser("spoken", parents=[commons], help="Conversation corpus")
    p_spoken.add_argument("--fields", type=str, nargs="+", default=["speakers", "sentences"], choices=SPOKEN_AVAILABLE_FIELDS)
    p_spoken.add_argument("-r", "--remove_masked_sentences", dest="remove_masked_sentences", action="store_true")
    p_spoken.add_argument("-c", "--concate_successive", dest="concate_successive", action="store_true")
    p_spoken.set_defaults(func=spoken_to_corpus)

    # Do task
    args = parser.parse_args()
    show_arguments(args)
    task_function = args.func
    task_function(args)


if __name__ == "__main__":
    main()
