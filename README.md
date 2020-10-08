# moducorpus-sanitizer: 모두의 말뭉치 정제

## Install

(from source)
```
git clone https://github.com/ko-nlp/moducorpus-sanitizer
cd moducorpus-sanitizer
python setup.py install
```

(with pip)
```
pip install moducorpus_sanitizer
```

## 모두의 말뭉치: 뉴스 말뭉치

```
moducorpus news \
  --input_dir ~/local/modu/National_Institute_Korean_Language/NIKL_NEWSPAPER\(v1.0\) \
  --output_dir ~/local/modu/sanitizer/NIKL_NEWSPAPER/ \
  --corpus type multiline \
  --field title paragraph

moducorpus news \
  --input_dir ~/local/modu/National_Institute_Korean_Language/NIKL_NEWSPAPER\(v1.0\) \
  --output_dir ~/local/modu/sanitizer/NIKL_NEWSPAPER/ \
  --corpus type doublespaceline \
  --field title paragraph topic
```

| Arguments | values |
| --- | --- |
| input_dir | path/to/NIKL_NEWSPAPER(v1.0) |
| output_dir | path/to/corpus/NIKL_NEWSPAPER |
| type | 다음 값 중 한가지 선택 ['multiline', 'doublespaceline' |
| fields | 다음 값 중 중복 선택 ['title', 'author', 'publisher', 'date', 'topic', 'original_topic', 'paragraph'] |

## 모두의 말뭉치: 메신저 말뭉치

```
moducorpus --debug messenger \
  --input_dir ~/local/modu/National_Institute_Korean_Language/NIKL_MESSENGER\(v1.0\) \
  --output_dir ~/local/modu/sanitizer/NIKL_MESSENGER/
```

| Arguments | values |
| --- | --- |
| input_dir | path/to/NIKL_MESSENGER(v1.0) |
| output_dir | path/to/corpus/NIKL_MESSENGER |
