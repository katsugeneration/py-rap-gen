# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Tone processing module."""


tone_types = {}
tone_types["a"] = ['ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'ガ', 'ザ', 'ダ', 'バ', 'パ', 'ャ', 'ァ']
tone_types["i"] = ['イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', 'リ', 'ギ', 'ジ', 'ヂ', 'ビ', 'ピ', 'ィ']
tone_types["u"] = ['ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'グ', 'ズ', 'ヅ', 'ブ', 'プ', 'ュ', 'ゥ', 'ヴ']
tone_types["e"] = ['エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', 'レ', 'ゲ', 'ゼ', 'デ', 'ベ', 'ペ', 'ェ']
tone_types["o"] = ['オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ゴ', 'ゾ', 'ド', 'ボ', 'ポ', 'ョ', 'ォ']
tone_types["xtu"] = ['ッ']
tone_types["n"] = ['ン']
mini = ['ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ャ', 'ュ', 'ョ']


def convert_tones(kana):
    """Convert katakana to tone.

    Args:
        kana (String): kana list.
    Return:
        tones (List[String]): tone list.
        splitted_kana (List[String]): splitted kana list.
    """
    tones = []
    splitted_kana = []
    for k in kana:
        if k in mini and len(tones) != 0:
            del tones[-1]
        for t in tone_types:
            if k in tone_types[t]:
                if k in mini and len(splitted_kana) != 0:
                    splitted_kana[-1] += k
                else:
                    splitted_kana.append(k)
                tones.append(t)
        if k == 'ー':
            if len(tones) != 0:
                splitted_kana.append(k)
                tones.append(tones[-1])
    return tones, splitted_kana
