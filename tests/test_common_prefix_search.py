from py_rap_gen import __version__
from nose.tools import ok_, eq_
from py_rap_gen import common_prefix_search


class TestDoubleArray:
    def test_careate(self):
        da = common_prefix_search.DoubleArray()
        da.craete(['abc'])
        eq_(da._base, [0, 0, 0, -1])
        eq_(da._check, [-1, 0, 1, 2])


    def test_careate_contain_common_prefix(self):
        da = common_prefix_search.DoubleArray()
        da.craete(['abc', 'adc'])
        eq_(da._base, [0, 0, 0, -1, 0])
        eq_(da._check, [-1, 0, 1, 2, 1])