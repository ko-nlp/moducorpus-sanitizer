from moducorpus_sanitizer.modu_mp import parse


def test_parse():
    sentence = {
        "id": "NWRW1800000022.417.1.1",
        "form": '[제주·서울] "세계환경수도 조성위해 10개년 실천계획 만들겠다" 김태환 지사 밝혀',
        "word": [
            {"id": 1, "form": "[제주·서울]", "begin": 0, "end": 7},
            {"id": 2, "form": '"세계환경수도', "begin": 8, "end": 15},
            {"id": 3, "form": "조성위해", "begin": 16, "end": 20},
            {"id": 4, "form": "10개년", "begin": 21, "end": 25},
            {"id": 5, "form": "실천계획", "begin": 26, "end": 30},
            {"id": 6, "form": '만들겠다"', "begin": 31, "end": 36},
            {"id": 7, "form": "김태환", "begin": 37, "end": 40},
            {"id": 8, "form": "지사", "begin": 41, "end": 43},
            {"id": 9, "form": "밝혀", "begin": 44, "end": 46},
        ],
        "morpheme": [
            {"id": 1, "form": "[", "label": "SS", "word_id": 1, "position": 1},
            {"id": 2, "form": "제주", "label": "NNP", "word_id": 1, "position": 2},
            {"id": 3, "form": "·", "label": "SP", "word_id": 1, "position": 3},
            {"id": 4, "form": "서울", "label": "NNP", "word_id": 1, "position": 4},
            {"id": 5, "form": "]", "label": "SS", "word_id": 1, "position": 5},
            {"id": 6, "form": '"', "label": "SS", "word_id": 2, "position": 1},
            {"id": 7, "form": "세계", "label": "NNG", "word_id": 2, "position": 2},
            {"id": 8, "form": "환경", "label": "NNG", "word_id": 2, "position": 3},
            {"id": 9, "form": "수도", "label": "NNG", "word_id": 2, "position": 4},
            {"id": 10, "form": "조성", "label": "NNG", "word_id": 3, "position": 1},
            {"id": 11, "form": "위하", "label": "VV", "word_id": 3, "position": 2},
            {"id": 12, "form": "아", "label": "EC", "word_id": 3, "position": 3},
            {"id": 13, "form": "10", "label": "SN", "word_id": 4, "position": 1},
            {"id": 14, "form": "개년", "label": "NNB", "word_id": 4, "position": 2},
            {"id": 15, "form": "실천", "label": "NNG", "word_id": 5, "position": 1},
            {"id": 16, "form": "계획", "label": "NNG", "word_id": 5, "position": 2},
            {"id": 17, "form": "만들", "label": "VV", "word_id": 6, "position": 1},
            {"id": 18, "form": "겠", "label": "EP", "word_id": 6, "position": 2},
            {"id": 19, "form": "다", "label": "EF", "word_id": 6, "position": 3},
            {"id": 20, "form": '"', "label": "SS", "word_id": 6, "position": 4},
            {"id": 21, "form": "김태환", "label": "NNP", "word_id": 7, "position": 1},
            {"id": 22, "form": "지사", "label": "NNG", "word_id": 8, "position": 1},
            {"id": 23, "form": "밝히", "label": "VV", "word_id": 9, "position": 1},
            {"id": 24, "form": "어", "label": "EF", "word_id": 9, "position": 2},
        ],
        "WSD": [],
    }

    words_answer = [
        "[제주·서울]",
        '"세계환경수도',
        "조성위해",
        "10개년",
        "실천계획",
        '만들겠다"',
        "김태환",
        "지사",
        "밝혀",
    ]
    morphemes_answer = [
        [("[", "SS"), ("제주", "NNP"), ("·", "SP"), ("서울", "NNP"), ("]", "SS")],
        [('"', "SS"), ("세계", "NNG"), ("환경", "NNG"), ("수도", "NNG")],
        [("조성", "NNG"), ("위하", "VV"), ("아", "EC")],
        [("10", "SN"), ("개년", "NNB")],
        [("실천", "NNG"), ("계획", "NNG")],
        [("만들", "VV"), ("겠", "EP"), ("다", "EF"), ('"', "SS")],
        [("김태환", "NNP")],
        [("지사", "NNG")],
        [("밝히", "VV"), ("어", "EF")],
    ]

    words, morphemes = parse(sentence)

    assert words == words_answer
    assert morphemes == morphemes_answer
