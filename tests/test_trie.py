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
        da = trie.DoubleArray([('a', 'b', 'c')])
        eq_(da._base, [0, 0, 0, -1])
        eq_(da._check, [-1, 0, 1, 2])

    def test_create_contain_common_prefix(self):
        da = trie.DoubleArray([('a', 'b', 'c'), ('a', 'd', 'c')])
        eq_(da._base, [0, 0, 0, -1, 2, -1])
        eq_(da._check, [-1, 0, 1, 2, 1, 4])

    def test_create_contain_common_postfix(self):
        da = trie.DoubleArray([('a', 'b', 'c'), ('d', 'b', 'c')])
        eq_(da._base, [0, 0, 0, -1, 3, 3, -1])
        eq_(da._check, [-1, 0, 1, 2, 0, 4, 5])

    def test_create_multichars(self):
        da = trie.DoubleArray([('しゃ', 'か', 'い')])
        eq_(da._base, [0, 0, 0, -1])
        eq_(da._check, [-1, 0, 1, 2])

    def test_search(self):
        da = trie.DoubleArray([('a', 'b', 'c')])
        result = da.search(['a'])
        eq_(result, [('a', 'b', 'c')])
        result = da.search(['a', 'b'])
        eq_(result, [('a', 'b', 'c')])
        result = da.search(['a', 'b', 'c'])
        eq_(result, [('a', 'b', 'c')])

    def test_search_case_non_result(self):
        da = trie.DoubleArray([('a', 'b', 'c')])
        result = da.search(['a', 'b', 'a'])
        eq_(result, [])
        result = da.search(['a', 'c'])
        eq_(result, [])
        result = da.search(['b'])
        eq_(result, [])

    def test_search_case_non_vocabulary(self):
        da = trie.DoubleArray([('a', 'b', 'c')])
        result = da.search(['a', 'b', 'd'])
        eq_(result, [])
        result = da.search(['a', 'd'])
        eq_(result, [])
        result = da.search(['d'])
        eq_(result, [])

    def test_search_case_two_words(self):
        da = trie.DoubleArray([('a', 'b', 'c'), ('a', 'b', 'd')])
        result = da.search(['a'])
        eq_(result, [('a', 'b', 'c'), ('a', 'b', 'd')])
        result = da.search(['a', 'b'])
        eq_(result, [('a', 'b', 'c'), ('a', 'b', 'd')])
        result = da.search(['a', 'b', 'c'])
        eq_(result, [('a', 'b', 'c')])

    def test_search_max_len(self):
        da = trie.DoubleArray([('a', 'd'), ('a', 'b', 'c')])
        result = da.search(['a'], max_len=1)
        eq_(result, [])
        result = da.search(['a'], max_len=2)
        eq_(result, [('a', 'd')])
        result = da.search(['a'], max_len=3)
        eq_(result, [('a', 'd'), ('a', 'b', 'c')])

    def test_search_max_len_over_word_length(self):
        da = trie.DoubleArray([('a', 'd'), ('a', 'b', 'c')])
        result = da.search(['a', 'd'], max_len=1)
        eq_(result, [])
        result = da.search(['a', 'd'], max_len=2)
        eq_(result, [('a', 'd')])

    def test_search_multichars(self):
        da = trie.DoubleArray([('しゃ', 'か', 'い')])
        result = da.search(['しゃ'])
        eq_(result, [('しゃ', 'か', 'い')])
        result = da.search(['しゃ', 'か'])
        eq_(result, [('しゃ', 'か', 'い')])
        result = da.search(['しゃ', 'か', 'い'])
        eq_(result, [('しゃ', 'か', 'い')])

    def test_search_over_checklen(self):
        da = trie.DoubleArray([('a', 'b', 'c'), ('a', 'd', 'c')])
        result = da.search(['a', 'd', 'd'])
        eq_(result, [])

    def test_prefix_search(self):
        da = trie.DoubleArray([('a'), ('a', 'b'), ('a', 'b', 'c')])
        result = da.prefix_search(['a'])
        eq_(result, [('a')])
        result = da.prefix_search(['a', 'b'])
        eq_(result, [('a'), ('a', 'b')])
        result = da.prefix_search(['a', 'b', 'c'])
        eq_(result, [('a'), ('a', 'b'), ('a', 'b', 'c')])

    def test_prefix_search_case_non_vocabulary(self):
        da = trie.DoubleArray([('a'), ('a', 'b'), ('a', 'b', 'c')])
        result = da.prefix_search(['b'])
        eq_(result, [])
        result = da.prefix_search(['a', 'd'])
        eq_(result, [('a')])
        result = da.prefix_search(['a', 'b', 'a'])
        eq_(result, [('a'), ('a', 'b')])

    def test_prefix_search_case_non_word_vocabulary(self):
        da = trie.DoubleArray([('a'), ('a', 'b', 'c')])
        result = da.prefix_search(['a', 'b', 'c', 'd'])
        eq_(result, [('a'), ('a', 'b', 'c')])

    def test_prefix_search_multichars(self):
        da = trie.DoubleArray([('しゃ', ), ('しゃ', 'か'), ('しゃ', 'か', 'い')])
        result = da.prefix_search(['しゃ'])
        eq_(result, [('しゃ', )])
        result = da.prefix_search(['しゃ', 'か'])
        eq_(result, [('しゃ',), ('しゃ', 'か')])
        result = da.prefix_search(['しゃ', 'か', 'い'])
        eq_(result, [('しゃ',), ('しゃ', 'か'), ('しゃ', 'か', 'い')])

    def test_prefix_search_over_checklen(self):
        da = trie.DoubleArray([('a', 'b', 'c'), ('a', 'd', 'c')])
        result = da.prefix_search(['a', 'd', 'd'])
        eq_(result, [])
