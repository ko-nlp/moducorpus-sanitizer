import argparse

from .about import __version__
from .modu_messenger import messenger_to_corpus
from .modu_newspaper import news_to_corpus
from .modu_spoken import spoken_to_corpus
from .modu_web import web_to_corpus
from .modu_written import written_to_corpus
from .modu_newspaper import AVAILABLE_FIELDS as NEWS_AVAILABLE_FIELDS
from .modu_spoken import AVAILABLE_FIELDS as SPOKEN_AVAILABLE_FIELDS
from .modu_web import AVAILABLE_FIELDS as WEB_AVAILABLE_FIELDS
from .modu_written import AVAILABLE_FIELDS as WRITTEN_AVAILABLE_FIELDS


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
    p_news.add_argument(
        "--fields", type=str, nargs="+", default=NEWS_AVAILABLE_FIELDS,
        choices=NEWS_AVAILABLE_FIELDS, help=" default (%(default)s), choices [%(choices)s]"
    )
    p_news.set_defaults(func=news_to_corpus)

    # Messenger
    p_messenger = subparsers.add_parser("messenger", parents=[commons], help="Messenger corpus")
    p_messenger.set_defaults(func=messenger_to_corpus)

    # Spoken
    p_spoken = subparsers.add_parser("spoken", parents=[commons], help="Conversation corpus")
    p_spoken.add_argument(
        "--fields", type=str, nargs="+", default=SPOKEN_AVAILABLE_FIELDS,
        choices=SPOKEN_AVAILABLE_FIELDS, help=" default (%(default)s), choices [%(choices)s]"
    )
    p_spoken.add_argument("-r", "--remove_masked_sentences", dest="remove_masked_sentences", action="store_true")
    p_spoken.add_argument("-c", "--concate_successive", dest="concate_successive", action="store_true")
    p_spoken.set_defaults(func=spoken_to_corpus)

    # Web
    p_web = subparsers.add_parser("web", parents=[commons], help="Web corpus")
    p_web.add_argument(
        "--fields", type=str, nargs="+", default=WEB_AVAILABLE_FIELDS,
        choices=WEB_AVAILABLE_FIELDS, help=" default (%(default)s), choices [%(choices)s]"
    )
    p_web.set_defaults(func=web_to_corpus)

    # Written
    p_written = subparsers.add_parser("written", parents=[commons], help="Written corpus")
    p_written.add_argument(
        "--fields", type=str, nargs="+", default=WRITTEN_AVAILABLE_FIELDS,
        choices=WRITTEN_AVAILABLE_FIELDS, help=" default (%(default)s), choices [%(choices)s]"
    )
    p_written.set_defaults(func=written_to_corpus)

    # Do task
    args = parser.parse_args()
    show_arguments(args)
    task_function = args.func
    task_function(args)


if __name__ == "__main__":
    main()
