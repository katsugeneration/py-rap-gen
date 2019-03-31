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
