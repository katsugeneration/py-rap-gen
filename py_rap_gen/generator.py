# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.

import random
import pickle
from py_rap_gen import mecab
from py_rap_gen import tone
from py_rap_gen import graph
import numpy as np


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


def measure_tail_match_num(word1, word2):
    """Return tail match num between word1 and word2

    Aarg:
        word1 (str): target first word.
        word2 (str): target second word.
    Return:
        match_num (int): tail match word numbers.
    """
    match_num = 0
    while match_num < len(word1) and match_num < len(word2):
        if word1[-1-match_num] == word2[-1-match_num]:
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
    tones, _ = tone.convert_tones(yomi)
    tones = "".join(tones)

    distances = [
        (
            max(measure_tail_match_num(tones, t),
                measure_initial_match_num(tones, t)),
            t)
        for t in tone_list
        if len(tones) == len(t)
    ]

    distance = sorted(distances, key=lambda x: x[0], reverse=True)[0]
    return tone_list[distance[1]]


def get_match_word_with_searcher(yomi, tone_list, prefix_searcher):
    """Return tone match words with common prefix searcher.

    Aarg:
        yomi (str): target word yomi.
        tone_list (str): tone dictionary.
        prefix_searcher (TrieBase): Trie prefix searcher class
    Return:
        words (List[String]): match word list.
    """
    tones, _ = tone.convert_tones(yomi)
    N = len(tones)
    result = []
    while len(tones) != 0:
        result = prefix_searcher.search(tones, max_len=N)
        if len(result) != 0:
            break
        tones = tones[:-1]

    if len(result) == 0:
        return []
    return tone_list[random.choice(result)]


def generate_rap(s, tone_list, prefix_searcher):
    """Return generated rap.

    Aarg:
        s (str): target sentence.
        tone_list (str): tone dictionary.
        prefix_searcher (TrieBase): Trie Prefix Searcher class
    Return:
        rap (str): generated rap
    """
    yomis = []
    for w in mecab.parse(s).words:
        if w.pos == "名詞" or w.pos == "形容詞" or w.pos == "動詞":
            yomis.append([w.surface, w.yomi, True])
        else:
            if 0.7 < random.random():
                yomis[-1][1] += w.yomi
                yomis[-1][2] = True
            else:
                yomis.append([w.surface, w.yomi, False])
    return "".join(
        [random.choice(get_match_word_with_searcher(yomi, tone_list, prefix_searcher))
         if is_yomi else surface
         for surface, yomi, is_yomi in yomis]
    )


def generate_rapv2(s, tone_list, prefix_searcher):
    """Return generated rap.

    Aarg:
        s (str): target sentence.
        tone_list (str): tone dictionary.
        prefix_searcher (TrieBase): Trie Prefix Searcher class
    Return:
        rap (str): generated rap
    """
    import cProfile
    import pstats
    pr = cProfile.Profile()
    pr.enable()
    tones = "".join(tone.convert_tones("".join(w.yomi for w in mecab.parse(s).words)))
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, tones)
    g.learner = graph.StructuredLearner()
    path = g.search_shortest_path()
    path = path[:-1]
    pr.disable()
    ps = pstats.Stats(pr).sort_stats(*["time", "calls"])
    ps.print_stats()
    return "".join(p.word for p in path)


def main():
    with open('mecab_tone_yomi.pkl', 'rb') as w:
        tone_list = pickle.load(w)
    with open('prefix_searcher.pkl', 'rb') as w:
        prefix_searcher = pickle.load(w)
    while True:
        print('Please Input Sentence:')
        sentence = input()
        print('\nOutput Sentence:')
        print(generate_rap(sentence, tone_list, prefix_searcher))
        print('\n')
