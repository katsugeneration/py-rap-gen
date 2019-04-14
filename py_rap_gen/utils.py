# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.

import random
import pickle
from py_rap_gen import mecab
import numpy as np


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
        chars = mecab.parse(k).words[0].yomi
        tones = "".join(_convert_tones(chars))
        if tones == "":
            continue
        if tones not in tone_list:
            tone_list[tones] = []
        tone_list[tones].append(k)

        # for k1 in counter['children'][k]['children']:
        #     chars1 = mecab.parse(k1).strip().split()[0]
        #     tones1 = "".join(_convert_tones(chars1))
        #     if tones1 == "":
        #         continue
        #     tones_double = tones + tones1
        #     if tones_double not in tone_list:
        #         tone_list[tones_double] = []
        #     tone_list[tones_double].append(k + k1)
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


def measure_initial_match_num(word1, word2):
    """Return head match num between word1 and word2

    Aarg:
        word1 (str): target first word.
        word2 (str): target second word.
    Return:
        match_num (int): head match word numbers.
    """
    match_num = 0
    while match_num < len(word1) and match_num < len(word2):
        if word1[match_num] == word2[match_num]:
            match_num += 1
        else:
            break
    return match_num


def get_match_word(yomi, tone_list):
    """Return tone match words to word.

    Aarg:
        yomi (str): target word yomi.
        tone_list (str): tone dictionary.
    Return:
        words (List[String]): match word list.
    """
    tones = "".join(_convert_tones(yomi))

    distances = []
    for t in tone_list:
        l = measure_levenshtein(tones, t)
        distances.append((l, t))

    distance = sorted(distances, key=lambda x: x[0])[0]
    return tone_list[distance[1]]


def generate_rap(s, tone_list):
    """Return generated rap.

    Aarg:
        s (str): target sentence.
        tone_list (str): tone dictionary.
    Return:
        rap (str): generated rap
    """
    return "".join(
        [random.choice(get_match_word(w.yomi, tone_list))
            if w.pos == "名詞" or w.pos == "形容詞" or w.pos == "動詞"
            else w.surface
            for w in mecab.parse(s).words]
    )

# with open('mecab_tone_2gram.pkl', 'wb') as w:
#     pickle.dump(_create_tone_list(counter), w, pickle.HIGHEST_PROTOCOL)

with open('mecab_tone_2gram.pkl', 'rb') as w:
    tone_list = pickle.load(w)
