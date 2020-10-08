import json
from dataclasses import dataclass
from glob import glob
from tqdm import tqdm
from typing import List

from .utils import append, check_dir, check_fields


# document_id is default
AVAILABLE_FIELDS = {'title', 'author', 'publisher', 'date', 'topic', 'original_topic', 'paragraph'}

def news_to_corpus(args):
    # List-up arguments
    input_dir = args.input_dir
    output_dir = args.output_dir
    corpus_type = args.type
    fields = args.fields

    # Check fields
    fields = check_fields(fields, AVAILABLE_FIELDS)
    fields.append('document_id')

    # Prepare output paths
    check_dir(output_dir)
    field_to_file = {field: f'{output_dir}/{field}.txt' for field in fields}

    # Prepare input files
    paths = sorted(glob(f'{input_dir}/N*RW*.json'))
    if args.debug:  # DEVELOP CODE
        paths = paths[:3]

    # Set paragraph format
    if corpus_type == 'doublespaceline':
        paragraph_formatter = to_doublespaceline
    else:
        paragraph_formatter = to_multiline

    # Do sanitization
    for i_doc, documents in enumerate(iterate_files(paths, paragraph_formatter)):
        mode = 'w' if i_doc == 0 else 'a'
        for field in fields:
            path = field_to_file[field]
            values = [getattr(doc, field) for doc in documents]
            append(path, values, mode)


def to_multiline(lines):
    return '\n'.join(lines) + '\n'


def to_doublespaceline(lines):
    return '  '.join(lines)


@dataclass
class ModuNews:
    document_id: str
    title: str
    author: str
    publisher: str
    date: str
    topic: str
    original_topic: str
    paragraph: List[str]


def document_to_a_news(document, paragraph_formatter):
    document_id = document['id']
    meta = document['metadata']
    title = meta['title']
    author = meta['author']
    publisher = meta['publisher']
    date = meta['date']
    topic = meta['topic']
    original_topic = meta['original_topic']
    paragraph = paragraph_formatter([p['form'] for p in document['paragraph']])
    return ModuNews(document_id, title, author, publisher, date, topic, original_topic, paragraph)


def iterate_files(paths, paragraph_formatter):
    for i_path, path in enumerate(paths):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        documents = data['document']
        desc = f'Transform to ModuNews {i_path + 1}/{len(paths)} files'
        total = len(documents)
        documents = [document_to_a_news(doc, paragraph_formatter) for doc in tqdm(documents, desc=desc, total=total)]
        yield documents
