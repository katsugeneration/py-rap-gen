from nose.tools import ok_, eq_
from py_rap_gen import graph
from py_rap_gen import common_prefix_search
import pickle

    
tone_list = {
    'a': ['あ', 'か', 'さ'],
    'ao': ['あお', 'かお', 'さと'],
    'aoi': ['あおい', 'さとみ'],
    'o': ['と'],
    'oi': ['とい', 'こい', 'とし'],
    'oio': ['たいよ', 'はいりょ'],
    'i': ['き', 'し'],
    'io': ['みこ', 'しお'],
    'oa': ['もか', 'もさ'],
}
prefix_searcher = common_prefix_search.DoubleArray(tone_list.keys())


def test_construct_graph():
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, 'aoioa')
    eq_([g.BOS], g.nodes[0])
    eq_(set([graph.Node(0, 'か'), graph.Node(0, 'あ'), graph.Node(0, 'さ')]), set(g.nodes[1]))
    eq_(set([graph.Node(0, 'あお'), graph.Node(0, 'かお'), graph.Node(0, 'さと'), graph.Node(1, 'と')]),
        set(g.nodes[2]))
    eq_([g.EOS], g.nodes[6])

def test_search_shortest_path():
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, 'aoioa')
    g.learner = graph.StructuredLearner()
    path = g.search_shortest_path()
    eq_('あおい', path[0].word)
    eq_('もか', path[1].word)

def test_structured_perceptron():
    learner = graph.StructuredPerceptron()
    learner.train([('aoioa', ['あお', 'し', 'もさ'])], prefix_searcher, tone_list)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, 'aoioa')
    g.learner = learner
    path = g.search_shortest_path()
    eq_('あお', path[0].word)
    eq_('し', path[1].word)
    eq_('もさ', path[2].word)

def test_structured_perceptron_multiple_sentence():
    learner = graph.StructuredPerceptron()
    learner.train([('aoioa',['あお', 'し', 'もさ']), ('aooa', ['あ', 'と', 'と', 'さ'])], prefix_searcher, tone_list)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, 'aoioa')
    g.learner = learner
    path = g.search_shortest_path()
    eq_('あお', path[0].word)
    eq_('し', path[1].word)
    eq_('もさ', path[2].word)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, 'aooa')
    g.learner = learner
    path = g.search_shortest_path()
    eq_('あ', path[0].word)
    eq_('と', path[1].word)
    eq_('と', path[2].word)
    eq_('さ', path[3].word)

def test_structured_perceptron_iterator():
    class iteratorWrapper():
        def __init__(self, func):
            self._func = func

        def __iter__(self):
            return self._func()

    def data():
        for s, d in [('aoioa',['あお', 'し', 'もさ']), ('aooa', ['あ', 'と', 'と', 'さ'])]:
            yield (s, d)

    learner = graph.StructuredPerceptron()
    learner.train(iteratorWrapper(data), prefix_searcher, tone_list)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, 'aoioa')
    g.learner = learner
    path = g.search_shortest_path()
    eq_('あお', path[0].word)
    eq_('し', path[1].word)
    eq_('もさ', path[2].word)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, 'aooa')
    g.learner = learner
    path = g.search_shortest_path()
    eq_('あ', path[0].word)
    eq_('と', path[1].word)
    eq_('と', path[2].word)
    eq_('さ', path[3].word)
