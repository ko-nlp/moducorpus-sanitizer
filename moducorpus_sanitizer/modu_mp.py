import json
import os
from glob import glob
from tqdm import tqdm


def parse(sentence):
    words = [word["form"] for word in sentence["word"]]
    morphemes = [[] for _ in range(len(words))]
    for morpheme in sentence["morpheme"]:
        morphemes[morpheme["word_id"] - 1].append((morpheme["form"], morpheme["label"]))
    return words, morphemes


def formatter_type_1(words, morphemes):
    strf = ""
    for word_i, morpheme_i in zip(words, morphemes):
        morph_tags = " + ".join(f"{m}/{t}" for m, t in morpheme_i)
        strf += f"{word_i}\t{morph_tags}\n"
    return strf


def mp_to_corpus(args):
    input_dir = args.input_dir
    output_dir = args.output_dir
    output_type = args.type

    nxmp_path = sorted(glob(f"{input_dir}/NXMP*"))
    if not nxmp_path:
        raise ValueError(f"Not found `NXMPxxxxxxxx` file")
    nxmp_path = nxmp_path[-1]

    with open(nxmp_path, encoding="utf-8") as f:
        data = json.load(f)
    documents = data["document"]
    sentences = [
        sentence for document in documents for sentence in document["sentence"]
    ]

    formatter = formatter_type_1

    os.makedirs(os.path.abspath(output_dir), exist_ok=True)
    with open(f"{output_dir}/NXMP_type1.txt", "w", encoding="utf-8") as f:
        desc = f"Transform to ModuMP"
        for sentence in tqdm(sentences, desc=desc, total=len(sentences)):
            words, morphemes = parse(sentence)
            f.write(f"{formatter(words, morphemes)}\n")
