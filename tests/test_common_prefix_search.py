from py_rap_gen import __version__
from nose.tools import ok_, eq_
from py_rap_gen import common_prefix_search


class TestTrieBase:
    def test_create(self):
        da = common_prefix_search.TrieBase(['abc'])
        eq_(da._table[0], [-1, 1])
        eq_(da._table[1], [-1, -1, 2])
        eq_(da._table[2], [-1, -1, -1, 3])

    def test_create_contain_common_prefix(self):
        da = common_prefix_search.TrieBase(['abc', 'adc'])
        eq_(da._table[0], [-1, 1])
        eq_(da._table[1], [-1, -1, 2, -1, 4])
        eq_(da._table[2], [-1, -1, -1, 3])
        eq_(da._table[4], [-1, -1, -1, 5])

    def test_create_contain_common_postfix(self):
        da = common_prefix_search.TrieBase(['abc', 'dbc'])
        eq_(da._table[0], [-1, 1, -1, -1, 4])
        eq_(da._table[1], [-1, -1, 2])
        eq_(da._table[2], [-1, -1, -1, 3])
        eq_(da._table[4], [-1, -1, 5])
        eq_(da._table[5], [-1, -1, -1, 6])


class TestDoubleArray:
    def test_create(self):
        da = common_prefix_search.DoubleArray()
        da.create(['abc'])
        eq_(da._base, [0, 0, 0, -1])
        eq_(da._check, [-1, 0, 1, 2])

    def test_create_contain_common_prefix(self):
        da = common_prefix_search.DoubleArray()
        da.create(['abc', 'adc'])
        eq_(da._base, [0, 0, 0, -1, 0])
        eq_(da._check, [-1, 0, 1, 2, 1])