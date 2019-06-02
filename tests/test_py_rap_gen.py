from py_rap_gen import __version__
from nose.tools import ok_, eq_
from py_rap_gen import generator


def test_version():
    assert __version__ == '0.1.0'


def test_measure_levenshtein():
    eq_(0, generator.measure_levenshtein('aaa', 'aaa'))
    eq_(1, generator.measure_levenshtein('aaa', 'aaab'))
    eq_(1, generator.measure_levenshtein('aaa', 'aac'))
    eq_(2, generator.measure_levenshtein('aaa', 'aacb'))


def test_get_match_word():
    tone_list = {
        "aaa": ['頭'],
        "aaaa": ['頭が', '頭は'],
        "uoi": ['動き'],
        "uoia": ['動きは'],
        "uoiau": ['動き出す']
    }
    eq_(['頭'], generator.get_match_word("サカサ", tone_list))
    eq_(['動き出す'], generator.get_match_word("ウゴキマス", tone_list))


def test_generate_rap():
    tone_list = {
        "aaa": ['頭'],
        "aaaa": ['頭が', '頭は'],
        "uoi": ['動き'],
        "uoia": ['動きは'],
        "uoiau": ['動き出す']
    }
    import pickle
    with open('prefix_searcher_da.pkl', 'rb') as w:
        prefix_searcher = pickle.load(w)
    ok_(generator.generate_rap("逆さが", tone_list, prefix_searcher).startswith('頭'))


def test_measure_initial_match_num():
    eq_(3, generator.measure_initial_match_num('aaa', 'aaa'))
    eq_(1, generator.measure_initial_match_num('aa', 'a'))
    eq_(0, generator.measure_initial_match_num('aaa', 'ccc'))
    eq_(2, generator.measure_initial_match_num('aaa', 'aacb'))
