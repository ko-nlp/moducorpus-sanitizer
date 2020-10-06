import os


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
