# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Yomi data preprocessing module.
"""
import subprocess
import os
import pandas as pd
import pathlib
import pickle
from py_rap_gen import utils
from py_rap_gen import common_prefix_search

NEOLOGD_PATH = "mecab-ipadic-neologd"
DICT_PATH = 'mecab_yomi.pkl'
TONE_PATH = 'mecab_tone_yomi.pkl'
PREFIX_SEARCHER_PATH = 'prefix_searcher.pkl'


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


def main():
    _dict = None
    if not os.path.exists(NEOLOGD_PATH):
        _build_neologd(NEOLOGD_PATH)
    if os.path.exists(NEOLOGD_PATH):
        _dict = _preprocess_dict(NEOLOGD_PATH)
        with open(DICT_PATH, 'wb') as w:
            pickle.dump(_dict, w, pickle.HIGHEST_PROTOCOL)
    if _dict is None and os.path.exists(DICT_PATH):
        with open(DICT_PATH, 'rb') as f:
            _dict = pickle.load(f)
    if _dict is not None:
        tone_list = utils._create_tone_list(_dict)
        with open(TONE_PATH, 'wb') as w:
            pickle.dump(tone_list, w, pickle.HIGHEST_PROTOCOL)
        prefix_searcher = common_prefix_search.TrieBase(tone_list.keys())
        with open(PREFIX_SEARCHER_PATH, 'wb') as w:
            pickle.dump(prefix_searcher, w, pickle.HIGHEST_PROTOCOL)
