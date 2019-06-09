from nose.tools import ok_, eq_
from py_rap_gen import mecab


def test_mecab_case1():
    sentence = mecab.parse("青い空")
    eq_(sentence.words[0].surface, "青い")
    eq_(sentence.words[0].pos, "形容詞")
    eq_(sentence.words[1].surface, "空")
    eq_(sentence.words[1].pos, "名詞")


def test_mecab_case2():
    sentence = mecab.parse("金縛りにあったように動けない")
    eq_(sentence.words[0].surface, "金縛り")
    eq_(sentence.words[0].pos, "名詞")
    eq_(sentence.words[1].surface, "に")
    eq_(sentence.words[1].pos, "助詞")
    eq_(sentence.words[2].surface, "あっ")
    eq_(sentence.words[2].base, "ある")
    eq_(sentence.words[2].pos, "動詞")
    eq_(sentence.words[3].surface, "た")
    eq_(sentence.words[3].pos, "助動詞")
    eq_(sentence.words[4].surface, "よう")
    eq_(sentence.words[4].pos, "名詞")
    eq_(sentence.words[5].surface, "に")
    eq_(sentence.words[5].pos, "助詞")
    eq_(sentence.words[6].surface, "動け")
    eq_(sentence.words[6].pos, "動詞")
    eq_(sentence.words[6].base, "動ける")
    eq_(sentence.words[7].surface, "ない")
    eq_(sentence.words[7].pos, "助動詞")


def test_mecab_case3():
    sentence = mecab.parse("ゲスの極み乙女。")
    eq_(sentence.words[0].surface, "ゲス")
    eq_(sentence.words[0].pos, "名詞")
    eq_(sentence.words[1].surface, "の")
    eq_(sentence.words[1].pos, "助詞")
    eq_(sentence.words[2].surface, "極み")
    eq_(sentence.words[2].pos, "名詞")
    eq_(sentence.words[3].surface, "乙女")
    eq_(sentence.words[3].pos, "名詞")
    eq_(sentence.words[4].surface, "。")
    eq_(sentence.words[4].pos, "記号")

def test_mecab_yomi_and_pronounce():
    sentence = mecab.parse("aaaa")
    eq_(sentence.words[0].yomi, "aaaa")
    eq_(sentence.words[0].pronounce, "aaaa")
    sentence = mecab.parse("君はまさに俺の太陽")
    eq_(sentence.words[1].yomi, "ハ")
    eq_(sentence.words[1].pronounce, "ワ")
    eq_(sentence.words[5].yomi, "タイヨウ")
    eq_(sentence.words[5].pronounce, "タイヨー")
    sentence = mecab.parse("気づいた")
    eq_(sentence.words[0].yomi, "キヅイ")
    eq_(sentence.words[0].pronounce, "キズイ")
