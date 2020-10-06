import json
from dataclasses import dataclass
from glob import glob
from tqdm import tqdm
from typing import List

from .utils import check_dir, check_fields


# document_id is default
AVAILABLE_FIELDS = {'title', 'author', 'publisher', 'date', 'topic', 'original_topic', 'paragraph'}

def news_to_corpus(args):
    input_dir = args.input_dir
    output_dir = args.output_dir
    corpus_type = args.type
    fields = args.fields

    fields = check_fields(fields, AVAILABLE_FIELDS)
    fields.append('document_id')

    check_dir(output_dir)

    field_to_file = {field: f'{output_dir}/{field}.txt' for field in fields}
    paths = sorted(glob(f'{input_dir}/N*RW*.json'))
    if args.debug:  # DEVELOP CODE
        paths = paths[:3]

    for documents in iterate_files(paths):
        for field in fields:
            path = field_to_file[field]
            values = [getattr(doc, field) for doc in documents]
            append(path, values)


def append(path, data):
    with open(path, 'a', encoding='utf-8') as f:
        for row in data:
            f.write(f'{row}\n')


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


def document_to_a_news(document):
    document_id = document['id']
    meta = document['metadata']
    title = meta['title']
    author = meta['author']
    publisher = meta['publisher']
    date = meta['date']
    topic = meta['topic']
    original_topic = meta['original_topic']
    paragraph = [p['form'] for p in document['paragraph']]
    return ModuNews(document_id, title, author, publisher, date, topic, original_topic, paragraph)


def iterate_files(paths):
    news = []
    for i_path, path in enumerate(paths):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        documents = data['document']
        desc = f'Transform to ModuNews {i_path + 1}/{len(paths)} files'
        total = len(documents)
        documents = [document_to_a_news(doc) for doc in tqdm(documents, desc=desc, total=total)]
        yield documents
