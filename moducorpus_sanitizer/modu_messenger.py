import json
from dataclasses import dataclass
from glob import glob
from tqdm import tqdm
from typing import List

from .utils import append, check_dir, check_fields


def messenger_to_corpus(args):
    # List-up arguments
    input_dir = args.input_dir
    output_dir = args.output_dir

    # Prepare output paths
    check_dir(output_dir)
    fields = {'document_id', 'speaker_id', 'time', 'original_form'}
    field_to_file = {field: f'{output_dir}/{field}.txt' for field in fields}

    # Prepare input files
    paths = sorted(glob(f'{input_dir}/M*RW*.json'))
    if args.debug:  # DEVELOP CODE
        paths = paths[:3]

    # Do sanitization
    for i_doc, documents in enumerate(iterate_files(paths)):
        mode = 'w' if i_doc == 0 else 'a'
        for field in fields:
            path = field_to_file[field]
            values = [getattr(doc, field) for doc in documents]
            append(path, values, mode)


@dataclass
class ModuMessenger:
    document_id: str
    speaker_id: str
    time: str
    original_form: str


def document_to_a_messenger(document):
    def transform(values):
        return '\n'.join([v.replace('\n', '  ') for v in values])

    utterance = document['utterance']
    columns = zip(*[(u['speaker_id'], u['time'], u['original_form']) for u in utterance])
    speaker_id, time, original_form = columns

    document_id = transform([document['id']] * len(speaker_id))
    speaker_id = transform(speaker_id)
    time = transform(time)
    original_form = transform(original_form)

    return ModuMessenger(document_id, speaker_id, time, original_form)


def iterate_files(paths):
    for i_path, path in enumerate(paths):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        documents = data['document']
        desc = f'Transform to ModuMessenger {i_path + 1}/{len(paths)} files'
        total = len(documents)
        documents = [document_to_a_messenger(doc) for doc in tqdm(documents, desc=desc, total=total)]
        yield documents