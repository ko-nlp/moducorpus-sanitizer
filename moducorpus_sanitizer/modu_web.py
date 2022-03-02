import json
import os
from dataclasses import dataclass
from glob import glob
from tqdm import tqdm
from typing import List

from .utils import check_dir, check_fields


# document_id is default
AVAILABLE_FIELDS = {"title", "author", "category", "url", "date", "paragraph"}


def web_to_corpus(args):
    # List-up arguments
    input_dir = args.input_dir
    check_dir(args.output_dir)
    if args.text_only:
        output_file = os.path.join(args.output_dir, "NIKL_WEB.text")
    else:
        output_file = os.path.join(args.output_dir, "NIKL_WEB.jsonl")
    fields = args.fields

    # Check fields
    fields = check_fields(fields, AVAILABLE_FIELDS)
    fields.append("document_id")

    # Prepare input files
    paths = sorted(glob(f"{input_dir}/E*RW*.json"))
    if args.debug:  # DEVELOP CODE
        paths = paths[:3]

    # Do sanitization
    for i_doc, documents in enumerate(iterate_files(paths, args.supress_error)):
        mode = "w" if i_doc == 0 else "a"
        with open(output_file, mode) as f:
            if args.text_only:
                for doc in documents:
                    paragraph = "\n".join(getattr(doc, "paragraph"))
                    f.write(f"{paragraph}\n")
            else:
                for doc in documents:
                    selected = {field: getattr(doc, field) for field in fields}
                    f.write(json.dumps(selected, ensure_ascii=False) + "\n")


@dataclass
class ModuWeb:
    document_id: str
    title: str
    author: str
    category: str
    url: str
    date: str
    paragraph: List[str]


def document_to_a_web(document, category):
    paragraph = [p["form"] for p in document["paragraph"]]
    return ModuWeb(
        document_id=document["id"],
        title=document["metadata"]["title"],
        author=document["metadata"]["author"],
        category=category,
        url=document["metadata"]["url"],
        date=document["metadata"]["date"],
        paragraph=paragraph
    )


def iterate_files(paths, supress_error):
    for path in tqdm(paths, total=len(paths), position=1, leave=True, desc="Sanitizing Web"):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            documents = data["document"]
            category = data["metadata"]["category"]
            total = len(documents)
            documents = [document_to_a_web(doc, category) for doc in tqdm(documents, total=total, position=0, leave=False)]
            yield documents
        except Exception as err:
            if not supress_error:
                tqdm.write(f"Found error at {path}\n{err}")
            continue
