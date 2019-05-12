from py_rap_gen import __version__
from nose.tools import ok_, eq_
from py_rap_gen import common_prefix_search


class TestTrieBase:
    def test_create(self):
        tb = common_prefix_search.TrieBase(['abc'])
        eq_(tb._table[0], [-1, 1])
        eq_(tb._table[1], [-1, -1, 2])
        eq_(tb._table[2], [-1, -1, -1, 3])

    def test_create_contain_common_prefix(self):
        tb = common_prefix_search.TrieBase(['abc', 'adc'])
        eq_(tb._table[0], [-1, 1])
        eq_(tb._table[1], [-1, -1, 2, -1, 4])
        eq_(tb._table[2], [-1, -1, -1, 3])
        eq_(tb._table[4], [-1, -1, -1, 5])

    def test_create_contain_common_postfix(self):
        tb = common_prefix_search.TrieBase(['abc', 'dbc'])
        eq_(tb._table[0], [-1, 1, -1, -1, 4])
        eq_(tb._table[1], [-1, -1, 2])
        eq_(tb._table[2], [-1, -1, -1, 3])
        eq_(tb._table[4], [-1, -1, 5])
        eq_(tb._table[5], [-1, -1, -1, 6])

    def test_search(self):
        tb = common_prefix_search.TrieBase(['abc'])
        result = tb.search('a')
        eq_(result, ['abc'])
        result = tb.search('ab')
        eq_(result, ['abc'])
        result = tb.search('abc')
        eq_(result, ['abc'])

    def test_search_case_non_result(self):
        tb = common_prefix_search.TrieBase(['abc'])
        result = tb.search('aba')
        eq_(result, [])
        result = tb.search('ac')
        eq_(result, [])
        result = tb.search('b')
        eq_(result, [])

    def test_search_case_non_vocabulary(self):
        tb = common_prefix_search.TrieBase(['abc'])
        result = tb.search('abd')
        eq_(result, [])
        result = tb.search('ad')
        eq_(result, [])
        result = tb.search('d')
        eq_(result, [])

    def test_search_case_two_words(self):
        tb = common_prefix_search.TrieBase(['abc', 'abd'])
        result = tb.search('a')
        eq_(result, ['abc', 'abd'])
        result = tb.search('ab')
        eq_(result, ['abc', 'abd'])
        result = tb.search('abc')
        eq_(result, ['abc'])


class TestDoubleArray:
    def test_create(self):
        da = common_prefix_search.DoubleArray(['abc'])
        eq_(da._base, [0, 0, 0, -1])
        eq_(da._check, [-1, 0, 1, 2])

    def test_create_contain_common_prefix(self):
        da = common_prefix_search.DoubleArray(['abc', 'adc'])
        eq_(da._base, [0, 0, 0, -1, 2, -1])
        eq_(da._check, [-1, 0, 1, 2, 1, 4])

    def test_search(self):
        da = common_prefix_search.DoubleArray(['abc'])
        result = da.search('a')
        eq_(result, ['abc'])
        result = da.search('ab')
        eq_(result, ['abc'])
        result = da.search('abc')
        eq_(result, ['abc'])