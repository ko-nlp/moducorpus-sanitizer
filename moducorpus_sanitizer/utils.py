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
