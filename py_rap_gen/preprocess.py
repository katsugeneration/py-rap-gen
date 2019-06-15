# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Yomi data preprocessing module.
"""
import subprocess
import pandas as pd
import pathlib
import pickle
import random
from py_rap_gen import tone
from py_rap_gen import counter
from py_rap_gen import trie
from py_rap_gen import graph
from py_rap_gen import mecab

TONE_PATH = 'mecab_tone_yomi.pkl'
PREFIX_SEARCHER_PATH = 'prefix_searcher.pkl'
COUNTER_2GRAM_PATH = 'counter_2gram.pkl'
LEARNER_PATH = 'learner.pkl'


def _build_neologd(path):
    """Build neologd dictionary."""
    ret = subprocess.call("git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git " + path, shell=True)
    if ret != 0:
        return False
    ret = subprocess.call("cd " + path + "; libexec/make-mecab-ipadic-neologd.sh", shell=True)
    if ret != 0:
        return False
    return True


def _preprocess_dict(path):
    """Extract base and yomi data from mecab dictionary."""
    headers = [
        "surface", "leftconnection", "rightconnection", "cost",
        "pos", "pos1", "pos2", "pos3", "conjugation1", "conjugation2",
        "base", "yomi", "pronounce"]
    _dict = None
    for p in pathlib.Path(path + "/build").glob('**/*.csv'):
        print("Processing:", p)
        df = pd.read_csv(p, names=headers, header=None)
        if _dict is None:
            _dict = df
        else:
            _dict = _dict.append(df, ignore_index=True)
    _dict = _dict[["surface", "yomi"]].to_dict(orient='records')
    return _dict


def _process_syntax(line):
    sentence = mecab.parse(line)
    result = []
    ret_kana = ""
    ret_pronounce = ""
    for word in sentence.words:
        if word.pos == '記号':
            continue

        if len(tone.convert_tones(word.pronounce)[0]) == 0:
            result.append(ret_kana + " " + ret_pronounce)
            ret_kana = ""
            ret_pronounce = ""
            continue
        elif word.pos1 == '接尾' or word.pos not in ['形容詞', '名詞', '動詞', '副詞']:
            ret_kana += word.surface
            ret_pronounce += word.pronounce
        else:
            result.append(ret_kana + " " + ret_pronounce)
            ret_kana = word.surface
            ret_pronounce = word.pronounce
    result.append(ret_kana + " " + ret_pronounce)
    return "\t".join(r for r in result if r != "")


def _mix_tone_and_kana(tones, kanas):
    """Return kana and tone mixes list.

    Args:
        tones (List[String]): tone splitted list.
        kanas (List[String]): kana splitted list.

    Return:
        ret (List[Tuple[String]]): kana and tone mixes list.
    """
    if len(tones) != len(kanas):
        return []

    ret = []

    if len(tones) == 1:
        ret.append(tuple(tones))
        ret.append(tuple(kanas))
    else:
        ret.append(tuple(tones[:-1] + [kanas[-1]]))
        ret.append(tuple(tones[:-2] + kanas[-2:]))
    if len(tones) >= 3:
        ret.append(tuple(tones))

    return ret


def _create_tone_list():
    """Return tone to string dictionary.

    Return:
        tone_list (Hash[String, List[String]]): tone to string dictionary.
    """

    def train_data():
        with open("data", 'r') as f:
            for line in f:
                line = line.strip()
                words = line.split('\t')
                words = filter(lambda w: w.strip() != '', words)
                yield from words

    def train_data_2gram(lcounter):
        g = graph.Graph()
        with open("data", 'r') as f:
            for line in f:
                line = line.strip()
                words = line.split('\t')
                words = filter(lambda w: w.strip() != '', words)
                words = [w if w in lcounter._items else graph.UNKNOW_WORD for w in words]
                words = [g.BOS.word] + words + [g.EOS.word]
                yield from [words[i].split()[0] + '_' + words[i+1].split()[0] for i in range(len(words) - 1)]

    lcounter = counter.LossyCounter(epsilon=1e-5*5)
    lcounter.count(train_data())
    lcounter_2gram = counter.LossyCounter(epsilon=1e-6)
    lcounter_2gram.count(train_data_2gram(lcounter))
    print(len(lcounter._items))
    print(len(lcounter_2gram._items))

    tone_list = {}
    count = 0
    for w in lcounter._items:
        chars = w.split()[1]
        tones, kana = tone.convert_tones(chars)

        if len(tones) == 0:
            count += 1
            continue
        if len(tones) != len(kana):
            count += 1
            continue

        for t in _mix_tone_and_kana(tones, kana):
            if t not in tone_list:
                tone_list[t] = []
            tone_list[t].append(w.split()[0])
    print("Remove Count:", count)
    print('Total Count:', sum(1 for t in tone_list for l in tone_list[t]))
    return tone_list, lcounter_2gram


def _train_graph(prefix_searcher, tone_list, lcounter_2gram):
    """Training Structured learner.

    Return:
        learner (StructuredLearner): Pretrained learner object.
    """
    class iteratorWrapper():
        def __init__(self, func):
            self._func = func

        def __iter__(self):
            return self._func()

    def train_data():
        count = 0
        with open("data_syntax2", 'r') as f:
            for line in f:
                if random.random() > 0.01:
                    continue
                count += 1
                line = line.strip()
                words = list(filter(lambda w: w.strip() != '', line.split('\t')))
                words = list(filter(lambda w: all(any(c in t for t in tone.tone_types.values()) for c in w.split()[1]), words))
                if len(words) == 0:
                    continue

                t = []
                ws = []
                for w in words:
                    tones, kanas = tone.convert_tones(w.split()[1])
                    if len(tones) == 0:
                        continue
                    tones[-1] = kanas[-1]
                    t.extend(tones)
                    ws.append(w.split()[0])
                    if len(t) >= 10:
                        yield t, ws
                        t = []
                        ws = []
                if len(t) != 0:
                    yield t, ws

    learner = graph.StructuredPerceptron()
    learner.N = 1e7
    learner.epochs = 1
    learner.construct_feature(list(lcounter_2gram._items))
    learner.train(iteratorWrapper(train_data), prefix_searcher, tone_list)
    return learner


def main():
    ret = subprocess.call("./download.sh", shell=True)
    if ret != 0:
        return False
    with open('data', 'w') as w:
        with open('articles.txt', 'r') as f:
            for line in f:
                w.write(_process_syntax(line) + '\n')
    tone_list, lcounter_2gram = _create_tone_list()
    with open(TONE_PATH, 'wb') as w:
        pickle.dump(tone_list, w, pickle.HIGHEST_PROTOCOL)
    with open(COUNTER_2GRAM_PATH, 'wb') as w:
        pickle.dump(lcounter_2gram, w, pickle.HIGHEST_PROTOCOL)
    prefix_searcher = trie.DoubleArray(tone_list.keys())
    with open(PREFIX_SEARCHER_PATH, 'wb') as w:
        pickle.dump(prefix_searcher, w, pickle.HIGHEST_PROTOCOL)
    learner = _train_graph(prefix_searcher, tone_list, lcounter_2gram)
    with open(LEARNER_PATH, 'wb') as w:
        pickle.dump(learner, w, pickle.HIGHEST_PROTOCOL)
