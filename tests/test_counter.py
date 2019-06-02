from py_rap_gen import __version__
from nose.tools import ok_, eq_
from py_rap_gen import counter


def test_lossy_counting():
    lc = counter.LossyCounter(epsilon=0.5)
    lc.count(['あ', 'い', 'あ', 'あ'])
    eq_({'あ': 3}, lc._items)