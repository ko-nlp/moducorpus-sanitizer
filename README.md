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
  --field title paragraph
```