import json
import os
from dataclasses import dataclass
from glob import glob
from tqdm import tqdm
from typing import List

from .utils import check_dir, check_fields


# document_id is default
AVAILABLE_FIELDS = {"title", "topic", "date", "speakers", "sentences"}


def spoken_to_corpus(args):
    # List-up arguments
    input_dir = args.input_dir
    check_dir(args.output_dir)
    if args.text_only:
        output_file = os.path.join(args.output_dir, "NIKL_COLLOQUIAL.text")
    else:
        output_file = os.path.join(args.output_dir, "NIKL_COLLOQUIAL.jsonl")
    fields = args.fields

    # Check fields
    fields = check_fields(fields, AVAILABLE_FIELDS)
    fields.append("document_id")

    # Prepare input files
    paths = sorted(glob(f"{input_dir}/S*RW*.json"))
    if args.debug:  # DEVELOP CODE
        paths = paths[:3]

    # Do sanitization
    iterator = iterate_files(paths, args.supress_error, args.remove_masked_sentences, args.concate_successive)
    for i_doc, documents in enumerate(iterator):
        mode = "w" if i_doc == 0 else "a"
        with open(output_file, mode) as f:
            if args.text_only:
                for doc in documents:
                    sentences = "\n".join(getattr(doc, "sentences"))
                    f.write(f"{sentences}\n")
            else:
                for doc in documents:
                    selected = {field: getattr(doc, field) for field in fields}
                    f.write(json.dumps(selected, ensure_ascii=False) + "\n")


@dataclass
class ModuConversation:
    document_id: str
    title: str
    topic: str
    date: str
    speakers: List[str]
    sentences: List[str]


def document_to_a_conversation(document, remove_masked_sentences, concate_successive):
    utterance = document["utterance"]
    speakers = [u["speaker_id"] for u in utterance]
    sentences = [u["original_form"] for u in utterance]
    if concate_successive:
        speakers_ = [None]
        sentences_ = [None]
        for p, t in zip(speakers, sentences):
            if speakers_[-1] == p:
                sentences_[-1] = f"{sentences_[-1]} {t}"
            else:
                speakers_.append(p)
                sentences_.append(t.strip())
        speakers, sentences = speakers_[1:], sentences_[1:]
    if remove_masked_sentences:
        pass_indices = [i for i, s in enumerate(sentences) if "&" not in s]
        speakers = [speakers[i] for i in pass_indices]
        sentences = [sentences[i] for i in pass_indices]
    return ModuConversation(
        document_id=document["id"],
        title=document["metadata"]["title"],
        topic=document["metadata"]["topic"],
        date=document["metadata"]["date"],
        speakers=speakers,
        sentences=sentences
    )


def iterate_files(paths, supress_error, remove_masked_sentences, concate_successive):
    for path in tqdm(paths, total=len(paths), position=1, leave=True, desc="Sanitizing Spoken"):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            documents = data["document"]
            total = len(documents)
            documents = [
                document_to_a_conversation(doc, remove_masked_sentences, concate_successive)
                for doc in tqdm(documents, total=total, position=0, leave=False)
            ]
            yield documents
        except Exception as err:
            if not supress_error:
                tqdm.write(f"Found error at {path}\n{err}")
            continue
