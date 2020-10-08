import os


def append(path, data, mode):
    with open(path, mode, encoding='utf-8') as f:
        for row in data:
            f.write(f'{row}\n')


def check_dir(dirname):
    os.makedirs(os.path.abspath(dirname), exist_ok=True)


def check_fields(inputs, available_fields):
    checked = []
    for input in sorted(inputs):
        if input not in available_fields:
            print(f'Found wrong field `{input}`. Sanitizer ignore the field')
        else:
            checked.append(input)
    return checked


def load_text(path):
    with open(path, encoding='utf-8') as f:
        docs = [doc.strip() for doc in f]
    return docs


def load_multiline_text(path):
    with open(path, encoding='utf-8') as f:
        docs = [doc.strip() for doc in f.read().split('\n\n')]
    return docs


def load_text_selectively(path, indices):
    """Assume that `indices` is sorted"""
    indices = set(indices)
    docs = []
    with open(path, encoding='utf-8') as f:
        for idx, doc in enumerate(f):
            if idx not in indices:
                continue
            docs.append(doc.strip())
    return docs


def load_multiline_text_selectively(path, indices):
    """Assume that `indices` is sorted"""
    indices = set(indices)
    idx = 0
    docs = []
    buffer = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            if idx in indices:
                buffer.append(line.strip())
            if line == '\n':
                idx += 1
                if buffer:
                    docs.append(buffer)
                    buffer = []
                continue
    return docs
