from py_rap_gen import __version__
from nose.tools import ok_, eq_
from py_rap_gen import trie


class TestTrieBase:
    def test_create(self):
        tb = trie.TrieBase([('a', 'b', 'c')])
        eq_(tb._table[0], [-1, 1])
        eq_(tb._table[1], [-1, -1, 2])
        eq_(tb._table[2], [-1, -1, -1, 3])

    def test_create_contain_common_prefix(self):
        tb = trie.TrieBase([('a', 'b', 'c'), ('a', 'd' ,'c')])
        eq_(tb._table[0], [-1, 1])
        eq_(tb._table[1], [-1, -1, 2, -1, 4])
        eq_(tb._table[2], [-1, -1, -1, 3])
        eq_(tb._table[4], [-1, -1, -1, 5])

    def test_create_contain_common_postfix(self):
        tb = trie.TrieBase([('a', 'b', 'c'), ('d', 'b' ,'c')])
        eq_(tb._table[0], [-1, 1, -1, -1, 4])
        eq_(tb._table[1], [-1, -1, 2])
        eq_(tb._table[2], [-1, -1, -1, 3])
        eq_(tb._table[4], [-1, -1, 5])
        eq_(tb._table[5], [-1, -1, -1, 6])

    def test_create_multichars(self):
        tb = trie.TrieBase([('しゃ', 'か', 'い')])
        eq_(tb._table[0], [-1, 1])
        eq_(tb._table[1], [-1, -1, 2])
        eq_(tb._table[2], [-1, -1, -1, 3])

    def test_search(self):
        tb = trie.TrieBase([('a', 'b', 'c')])
        result = tb.search(['a'])
        eq_(result, [('a', 'b', 'c')])
        result = tb.search(['a', 'b'])
        eq_(result, [('a', 'b', 'c')])
        result = tb.search(['a', 'b', 'c'])
        eq_(result, [('a', 'b', 'c')])

    def test_search_case_non_result(self):
        tb = trie.TrieBase([('a', 'b', 'c')])
        result = tb.search(['a', 'b', 'a'])
        eq_(result, [])
        result = tb.search(['a', 'c'])
        eq_(result, [])
        result = tb.search(['b'])
        eq_(result, [])

    def test_search_case_non_vocabulary(self):
        tb = trie.TrieBase([('a', 'b', 'c')])
        result = tb.search(['a', 'b', 'd'])
        eq_(result, [])
        result = tb.search(['a', 'd'])
        eq_(result, [])
        result = tb.search(['d'])
        eq_(result, [])

    def test_search_case_two_words(self):
        tb = trie.TrieBase([('a', 'b', 'c'), ('a', 'b', 'd')])
        result = tb.search(['a'])
        eq_(result, [('a', 'b', 'c'), ('a', 'b', 'd')])
        result = tb.search(['a', 'b'])
        eq_(result, [('a', 'b', 'c'), ('a', 'b', 'd')])
        result = tb.search(['a', 'b', 'c'])
        eq_(result, [('a', 'b', 'c')])

    def test_search_multichars(self):
        tb = trie.TrieBase([('しゃ', 'か', 'い')])
        result = tb.search(['しゃ'])
        eq_(result, [('しゃ', 'か', 'い')])
        result = tb.search(['しゃ', 'か'])
        eq_(result, [('しゃ', 'か', 'い')])
        result = tb.search(['しゃ', 'か', 'い'])
        eq_(result, [('しゃ', 'か', 'い')])


class TestDoubleArray:
    def test_create(self):
        da = trie.DoubleArray(['abc'])
        eq_(da._base, [0, 0, 0, -1])
        eq_(da._check, [-1, 0, 1, 2])

    def test_create_contain_common_prefix(self):
        da = trie.DoubleArray(['abc', 'adc'])
        eq_(da._base, [0, 0, 0, -1, 2, -1])
        eq_(da._check, [-1, 0, 1, 2, 1, 4])

    def test_create_contain_common_postfix(self):
        da = trie.DoubleArray(['abc', 'dbc'])
        eq_(da._base, [0, 0, 0, -1, 3, 3, -1])
        eq_(da._check, [-1, 0, 1, 2, 0, 4, 5])

    def test_search(self):
        da = trie.DoubleArray(['abc'])
        result = da.search('a')
        eq_(result, ['abc'])
        result = da.search('ab')
        eq_(result, ['abc'])
        result = da.search('abc')
        eq_(result, ['abc'])

    def test_search_case_non_result(self):
        da = trie.DoubleArray(['abc'])
        result = da.search('aba')
        eq_(result, [])
        result = da.search('ac')
        eq_(result, [])
        result = da.search('b')
        eq_(result, [])

    def test_search_case_non_vocabulary(self):
        da = trie.DoubleArray(['abc'])
        result = da.search('abd')
        eq_(result, [])
        result = da.search('ad')
        eq_(result, [])
        result = da.search('d')
        eq_(result, [])

    def test_search_case_two_words(self):
        da = trie.DoubleArray(['abc', 'abd'])
        result = da.search('a')
        eq_(result, ['abc', 'abd'])
        result = da.search('ab')
        eq_(result, ['abc', 'abd'])
        result = da.search('abc')
        eq_(result, ['abc'])

    def test_search_max_len(self):
        da = trie.DoubleArray(['ad', 'abc'])
        result = da.search('a', max_len=1)
        eq_(result, [])
        result = da.search('a', max_len=2)
        eq_(result, ['ad'])
        result = da.search('a', max_len=3)
        eq_(result, ['ad', 'abc'])

    def test_search_max_len_over_word_length(self):
        da = trie.DoubleArray(['ad', 'abc'])
        result = da.search('ad', max_len=1)
        eq_(result, [])
        result = da.search('ad', max_len=2)
        eq_(result, ['ad'])

    def test_prefix_search(self):
        da = trie.DoubleArray(['a', 'ab', 'abc'])
        result = da.prefix_search('a')
        eq_(result, ['a'])
        result = da.prefix_search('ab')
        eq_(result, ['a', 'ab'])
        result = da.prefix_search('abc')
        eq_(result, ['a', 'ab', 'abc'])

    def test_prefix_search_case_non_vocabulary(self):
        da = trie.DoubleArray(['a', 'ab', 'abc'])
        result = da.prefix_search('b')
        eq_(result, [])
        result = da.prefix_search('ad')
        eq_(result, ['a'])
        result = da.prefix_search('aba')
        eq_(result, ['a', 'ab'])

    def test_prefix_search_case_non_word_vocabulary(self):
        da = trie.DoubleArray(['a', 'abc'])
        result = da.prefix_search('abcd')
        eq_(result, ['a', 'abc'])
