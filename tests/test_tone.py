from py_rap_gen import __version__
from nose.tools import ok_, eq_
from py_rap_gen import tone


def testconvert_tones():
    eq_((['e', 'i', 'a', 'i'], ['セ', 'イ', 'タ', 'イ']), tone.convert_tones('セイタイ'))
    eq_((['a', 'u', 'xtu'], ['ヤ', 'ブ', 'ッ']), tone.convert_tones('ヤブッ'))
    eq_((['a', 'i', 'o', 'u', 'i', 'a'], ['カ', 'リ', 'フォ', 'ル', 'ニ', 'ア']), tone.convert_tones('カリフォルニア'))
    eq_((['o', 'u', 'e', 'u'], ['チョ', 'ウ', 'セ', 'ツ']), tone.convert_tones('チョウセツ'))
    eq_((['o', 'o', 'a', 'e', 'i', 'o', 'u'], ['ロ', 'ー', 'マ', 'テ', 'イ', 'コ', 'ク']), tone.convert_tones('ローマテイコク'))
    eq_(([], []), tone.convert_tones('、'))
    eq_((['a', 'n', 'a', 'n'], ['カ', 'ン', 'タ', 'ン']), tone.convert_tones('カンタン'))
    eq_((['a', 'a', 'a'], ['カ', 'ラ', 'ー']), tone.convert_tones('カラー'))
    eq_(([], []), tone.convert_tones('ー'))
    eq_((['a', 'n', 'a', 'i', 'a'], ['ヴァ', 'ン', 'パ', 'イ', 'ア']), tone.convert_tones('ヴァンパイア'))
    eq_((['o'], ['ョ']), tone.convert_tones('ョ'))


def testconvert_tones_error_case():
    eq_(([], []), tone.convert_tones('aaaa'))
