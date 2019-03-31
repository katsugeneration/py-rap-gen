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
        "aaa": ['頭'],
        # "aaaa": ['頭が', '頭は'],
        "uoi": ['動き'],
        # "uoia": ['動きは'],
        # "uoiau": ['動き出す']
    }
    eq_(expected, ret)


def test_measure_levenshtein():
    eq_(0, utils.measure_levenshtein('aaa', 'aaa'))
    eq_(1, utils.measure_levenshtein('aaa', 'aaab'))
    eq_(1, utils.measure_levenshtein('aaa', 'aac'))
    eq_(2, utils.measure_levenshtein('aaa', 'aacb'))


def test_get_match_word():
    tone_list = {
        "aaa": ['頭'],
        "aaaa": ['頭が', '頭は'],
        "uoi": ['動き'],
        "uoia": ['動きは'],
        "uoiau": ['動き出す']
    }
    eq_(['頭'], utils.get_match_word("逆さ", tone_list))
    eq_(['動き出す'], utils.get_match_word("動き出すか", tone_list))
