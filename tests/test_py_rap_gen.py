from py_rap_gen import __version__
from nose.tools import ok_, eq_
from py_rap_gen import utils


def test_version():
    assert __version__ == '0.1.0'

def test_convert_tones():
    eq_(['e', 'i', 'a', 'i'], utils._convert_tones('セイタイ'))
    eq_(['a', 'u', 'xtu'], utils._convert_tones('ヤブッ'))
    eq_(['a', 'i', 'o', 'u', 'i', 'a'], utils._convert_tones('カリフォルニア'))
    eq_(['o', 'u', 'e', 'u'], utils._convert_tones('チョウセツ'))
    eq_(['o', 'a', 'e', 'i', 'o', 'u'], utils._convert_tones('ローマテイコク'))
    eq_([], utils._convert_tones('、'))
    eq_(['a', 'n', 'a', 'n'], utils._convert_tones('カンタン'))

def test_create_tone_list():
    counter = {
        'children': {
            '頭': {
                'children': {
                    'が': {

                    },
                    'は': {

                    }
                }
            },
            '動き': {
                'children': {
                    'は': {

                    },
                    '出す': {
                        
                    }
                }
            }
        }
    }
    ret = utils._create_tone_list(counter)
    expected = {
        "aaa": ['アタマ'],
        "aaaa": ['アタマガ', 'アタマハ'],
        "uoi": ['ウゴキ'],
        "uoia": ['ウゴキハ'],
        "uoiau": ['ウゴキダス']
    }
    eq_(expected, ret)


def test_measure_levenshtein():
    eq_(0, utils.measure_levenshtein('aaa', 'aaa'))
    eq_(1, utils.measure_levenshtein('aaa', 'aaab'))
    eq_(1, utils.measure_levenshtein('aaa', 'aac'))
    eq_(2, utils.measure_levenshtein('aaa', 'aacb'))


def test_get_match_word():
    tone_list = {
        "aaa": ['アタマ'],
        "aaaa": ['アタマガ', 'アタマハ'],
        "uoi": ['ウゴキ'],
        "uoia": ['ウゴキハ'],
        "uoiau": ['ウゴキダス']
    }
    eq_(['アタマ'], utils.get_match_word("逆さ", tone_list))
    eq_(['ウゴキダス'], utils.get_match_word("動き出すか", tone_list))
