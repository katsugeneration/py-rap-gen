# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Yomi data preprocessing module.
"""
import subprocess
import os
import pandas as pd
import pathlib
import pickle

NEOLOGD_PATH = "mecab-ipadic-neologd"


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
    values = None
    for p in pathlib.Path(path + "/build").glob('**/*.csv'):
        print("Processing:", p)
        df = pd.read_csv(p, names=headers, header=None)
        if values is None:
            values = df
        else:
            values = values.append(df, ignore_index=True)
    values = values[["surface", "yomi"]].to_dict(orient='records')
    with open('mecab_1gram.pkl', 'wb') as w:
        pickle.dump(values, w, pickle.HIGHEST_PROTOCOL)


def main():
    if not os.path.exists(NEOLOGD_PATH):
        _build_neologd(NEOLOGD_PATH)
    if os.path.exists(NEOLOGD_PATH):
        _preprocess_dict(NEOLOGD_PATH)


if __name__ == '__main__':
    main()
