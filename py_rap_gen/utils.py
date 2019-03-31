# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.

import pickle
import MeCab
import numpy as np


mecab = MeCab.Tagger("-F%f[7]\s -U\s")

with open('mecab_2gram.pkl', 'rb') as f:
    counter = pickle.load(f)

tone_types = {}
tone_types["a"] = ['ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'ガ', 'ザ', 'ダ', 'バ', 'パ', 'ャ', 'ァ']
tone_types["i"] = ['イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', 'リ', 'ギ', 'ジ', 'ヂ', 'ビ', 'ピ', 'ィ']
tone_types["u"] = ['ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'グ', 'ズ', 'ヅ', 'ブ', 'プ', 'ュ', 'ゥ']
tone_types["e"] = ['エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', 'レ', 'ゲ', 'ゼ', 'デ', 'ベ', 'ペ', 'ェ']
tone_types["o"] = ['オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ゴ', 'ゾ', 'ド', 'ボ', 'ポ', 'ョ', 'ォ']
tone_types["xtu"] = ['ッ']
tone_types["n"] = ['ン']
mini = ['ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ャ', 'ュ', 'ョ']


def _convert_tones(kana):
    """Convert katakana to tone.

    Args:
        kana (List[String]): kana list.
    Return:
        tones (List[String]): tone list.
    """
    tones = []
    for k in kana:
        if k in mini and len(tones) != 0:
            del tones[-1]
        for t in tone_types:
            if k in tone_types[t]:
                tones.append(t)
    return tones


def _create_tone_list(counter):
    """Return tone to string dictionary.

    Return:
        tone_list (Hash[String, List[String]]): tone to string dictionary.
    """
    tone_list = {}
    for k in counter['children']:
        chars = mecab.parse(k).strip().split()[0]
        tones = "".join(_convert_tones(chars))
        if tones == "":
            continue
        if tones not in tone_list:
            tone_list[tones] = []
        tone_list[tones].append(chars)

        for k1 in counter['children'][k]['children']:
            chars1 = mecab.parse(k1).strip().split()[0]
            tones1 = "".join(_convert_tones(chars1))
            if tones1 == "":
                continue
            tones_double = tones + tones1
            if tones_double not in tone_list:
                tone_list[tones_double] = []
            tone_list[tones_double].append(chars + chars1)
    return tone_list


def measure_levenshtein(word1, word2):
    """Return levenshtein distance between word1 and word2

    Aarg:
        word1 (str): target first word.
        word2 (str): target second word.
    Return:
        distance (int): levenshtein distance between word1 and word2.
    """
    l_w1 = len(word1)
    l_w2 = len(word2)
    distances = np.zeros((l_w1 + 1, l_w2 + 1), dtype=np.int32)

    for i in range(l_w1 + 1):
        distances[i][0] = i

    for j in range(l_w2 + 1):
        distances[0][j] = j

    for i in range(1, l_w1 + 1):
        for j in range(1, l_w2 + 1):
            x = 1
            if word1[i - 1] == word2[j - 1]:
                x = 0

            distances[i][j] = min(
                distances[i - 1][j] + 1,
                distances[i][j - 1] + 1,
                distances[i - 1][j - 1] + x)
    return distances[l_w1][l_w2]


def get_match_word(word, tone_list):
    """Return tone match words to word.

    Aarg:
        word (str): target word.
        tone_list (str): tone dictionary.
    Return:
        words (List[String]): match word list.
    """
    chars = mecab.parse(word).strip().split()[0]
    tones = "".join(_convert_tones(chars))

    distances = []
    for t in tone_list:
        l = measure_levenshtein(tones, t)
        distances.append((l, t))

    distance = sorted(distances, key=lambda x: x[0])[0]
    return tone_list[distance[1]]


with open('mecab_tone_2gram.pkl', 'rb') as w:
    tone_list = pickle.load(w)

import random
for w in ['君', 'は', 'まるで', '俺', 'の', '太陽']:
    print(random.choice(get_match_word(w, tone_list)))
