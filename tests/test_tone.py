from py_rap_gen import __version__
from nose.tools import ok_, eq_
from py_rap_gen import tone


def testconvert_tones():
    eq_(['e', 'i', 'a', 'i'], tone.convert_tones('セイタイ'))
    eq_(['a', 'u', 'xtu'], tone.convert_tones('ヤブッ'))
    eq_(['a', 'i', 'o', 'u', 'i', 'a'], tone.convert_tones('カリフォルニア'))
    eq_(['o', 'u', 'e', 'u'], tone.convert_tones('チョウセツ'))
    eq_(['o', 'o', 'a', 'e', 'i', 'o', 'u'], tone.convert_tones('ローマテイコク'))
    eq_([], tone.convert_tones('、'))
    eq_(['a', 'n', 'a', 'n'], tone.convert_tones('カンタン'))
    eq_(['a', 'a', 'a'], tone.convert_tones('カラー'))
    eq_([], tone.convert_tones('ー'))
    eq_(['a', 'n', 'a', 'i', 'a'], tone.convert_tones('ヴァンパイア'))