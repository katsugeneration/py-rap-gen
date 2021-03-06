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
        ("a", "a", "a"): ['頭'],
        ("a", "a", "a", "a"): ['頭が', '頭は'],
        ("u", "o", "i"): ['動き'],
        ("u", "o", "i", "a"): ['動きは'],
        ("u", "o", "i", "a", "u"): ['動き出す']
    }
    eq_(['頭'], generator.get_match_word("サカサ", tone_list))
    eq_(['動き出す'], generator.get_match_word("ウゴキマス", tone_list))


def test_measure_initial_match_num():
    eq_(3, generator.measure_initial_match_num('aaa', 'aaa'))
    eq_(1, generator.measure_initial_match_num('aa', 'a'))
    eq_(0, generator.measure_initial_match_num('aaa', 'ccc'))
    eq_(2, generator.measure_initial_match_num('aaa', 'aacb'))
