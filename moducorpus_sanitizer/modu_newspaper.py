import json
import os
from dataclasses import dataclass
from glob import glob
from tqdm import tqdm
from typing import List

from .utils import check_dir, check_fields


# document_id is default
AVAILABLE_FIELDS = {'title', 'author', 'publisher', 'date', 'topic', 'original_topic', 'paragraph'}

def news_to_corpus(args):
    # List-up arguments
    input_dir = args.input_dir
    check_dir(args.output_dir)
    if args.text_only:
        output_file = os.path.join(args.output_dir, 'NIKL_NEWSPAPER.text')
    else:
        output_file = os.path.join(args.output_dir, 'NIKL_NEWSPAPER.jsonl')
    fields = args.fields

    # Check fields
    fields = check_fields(fields, AVAILABLE_FIELDS)
    fields.append('document_id')

    # Prepare input files
    paths = sorted(glob(f'{input_dir}/N*RW*.json'))
    if args.debug:  # DEVELOP CODE
        paths = paths[:3]

    # Do sanitization
    for i_doc, documents in enumerate(iterate_files(paths)):
        mode = 'w' if i_doc == 0 else 'a'
        with open(output_file, mode) as f:
            if args.text_only:
                for doc in documents:
                    f.write(getattr(doc, "paragraph") + "\n")
            else:
                for doc in documents:
                    selected = {field: getattr(doc, field) for field in fields}
                    f.write(json.dumps(selected, ensure_ascii=False) + "\n")


@dataclass
class ModuNews:
    document_id: str
    title: str
    author: str
    publisher: str
    date: str
    topic: str
    original_topic: str
    paragraph: str


def document_to_a_news(document):
    document_id = document['id']
    meta = document['metadata']
    title = meta['title']
    author = meta['author']
    publisher = meta['publisher']
    date = meta['date']
    topic = meta['topic']
    original_topic = meta['original_topic']
    paragraph = "\n".join([p['form'] for p in document['paragraph']])
    return ModuNews(document_id, title, author, publisher, date, topic, original_topic, paragraph)


def iterate_files(paths):
    for path in tqdm(paths, total=len(paths), position=1, leave=True, desc="Transform to ModuNews"):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        documents = data['document']
        total = len(documents)
        documents = [document_to_a_news(doc) for doc in tqdm(documents, total=total, position=0,leave=False)]
        yield documents
