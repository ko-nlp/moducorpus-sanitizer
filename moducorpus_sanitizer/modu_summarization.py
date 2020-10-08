import json
from tqdm import tqdm

from .utils import load_text


def summarization_to_corpus(args):
    news_corpus_dir = args.news_corpus_dir
    summarization_input_dir = args.summarization_input_dir
    output_dir = args.output_dir

    # Load news document id to row index mapper
    document_id_path = os.path.join(news_corpus_dir, 'document_id.txt')
    document_ids = load_text(document_id_path)
    document_id_to_row = {ids: row for row, ids in enumerate(document_ids)}

    # Load summarization raw data
    summarization_data_path = os.path.join(summarization_input_dir, 'NIKL_SC.json')
    with open(summarization_data_path, encoding='utf-8') as f:
        summarization_json_data = json.load(f)

    data = summarization_json_data['data']
    # TODO: found is not sorted. Resolve it
    found = []
    for sum_doc in tqdm(data, desc='check', total=len(data)):
        if sum_doc['document_id'] not in row_to_document_ids:
            continue
        founds.append(sum_doc['document_id'])
    news_indices = [document_id_to_row[idx] for idx in founds]

    # Load matched news
    # TODO: option: multiline or doublespaceline
    news_corpus_path = os.path.join(news_corpus_dir, 'paragraph.txt')
    news = load_multiline_text_selectively(news_corpus_path, news_indices)

    raise NotImplementedError
