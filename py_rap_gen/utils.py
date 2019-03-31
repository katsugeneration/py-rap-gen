# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.

import pickle
import MeCab

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
mini = ['ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ャ', 'ュ', 'ョ']


def _convert_tones(kana):
    tones = []
    for k in kana:
        if k in mini and len(tones) != 0:
            del tones[-1]
        for t in tone_types:
            if k in tone_types[t]:
                tones.append(t)
    return tones

for k in counter['children']:
    a = mecab.parse(k).strip().split()[0]
    print(a)
    print(_convert_tones(a))
