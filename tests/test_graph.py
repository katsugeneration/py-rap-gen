from nose.tools import ok_, eq_, raises
from py_rap_gen import graph
from py_rap_gen import trie
import pickle

    
tone_list = {
    ('a',): ['あ', 'か', 'さ'],
    ('a', 'o'): ['あお', 'かお', 'さと'],
    ('a', 'o', 'i'): ['あおい', 'さとみ'],
    ('o',): ['と'],
    ('o', 'i'): ['とい', 'こい', 'とし'],
    ('o', 'i', 'o'): ['たいよ', 'はいりょ'],
    ('i',): ['き', 'し'],
    ('i', 'o'): ['みこ', 'しお'],
    ('o', 'a'): ['もか', 'もさ'],
}
prefix_searcher = trie.DoubleArray(tone_list.keys())


def test_construct_graph():
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'i', 'o', 'a'))
    eq_([g.BOS], g.nodes[0])
    eq_(set([graph.Node(0, 'か'), graph.Node(0, 'あ'), graph.Node(0, 'さ')]), set(g.nodes[1]))
    eq_(set([graph.Node(0, 'あお'), graph.Node(0, 'かお'), graph.Node(0, 'さと'), graph.Node(1, 'と')]),
        set(g.nodes[2]))
    eq_([g.EOS], g.nodes[6])

def test_search_shortest_path():
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'i', 'o', 'a'))
    g.learner = graph.StructuredLearner()
    path = g.search_shortest_path()
    eq_('あおい', path[0].word)
    eq_('もか', path[1].word)

@raises(graph.SearchShortestPathError)
def test_search_shortest_path_non_vocabulary():
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'u', 'o', 'a'))
    g.learner = graph.StructuredLearner()
    path = g.search_shortest_path()

def test_search_nbest_path():
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'i', 'o', 'a'))
    g.learner = graph.StructuredLearner()
    g.learner.construct_feature(['あおい', 'もか'])
    g.learner._w[g.learner._feature2index['あおい']] = 99
    g.learner._w[g.learner._feature2index['もか']] = 99
    shortest_path = g.search_shortest_path()
    path = g.search_nbest_path(1)
    eq_(1, len(path))
    eq_(shortest_path[0].word, path[0][0].word)
    eq_(shortest_path[1].word, path[0][1].word)

def test_search_nbest_path_case_2():
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'i', 'o', 'a'))
    g.learner = graph.StructuredLearner()
    g.learner.construct_feature(['あおい', 'さとみ', 'もか', 'さとみ_もか', 'あおい_もか'])
    g.learner._w[g.learner._feature2index['あおい']] = 99
    g.learner._w[g.learner._feature2index['さとみ']] = 99
    g.learner._w[g.learner._feature2index['もか']] = 99
    g.learner._w[g.learner._feature2index['さとみ_もか']] = 1
    g.learner._w[g.learner._feature2index['あおい_もか']] = 0
    shortest_path = g.search_shortest_path()
    path = g.search_nbest_path(2)
    eq_(2, len(path))
    eq_(shortest_path[0].word, path[0][0].word)
    eq_(shortest_path[1].word, path[0][1].word)
    eq_('さとみ', path[1][0].word)
    eq_('もか', path[1][1].word)

def test_structured_perceptron_gold_contains_non_vocabulary():
    learner = graph.StructuredPerceptron()
    learner.train([(('a', 'o', 'i', 'o', 'a'),['あお', 'し', 'もさ']), (('a', 'o', 'o', 'a'), ['た', 'と', 'と', 'さ'])], prefix_searcher, tone_list)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'i', 'o', 'a'))
    g.learner = learner
    path = g.search_shortest_path()
    eq_('あお', path[0].word)
    eq_('し', path[1].word)
    eq_('もさ', path[2].word)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'o', 'a'))
    g.learner = learner
    path = g.search_shortest_path()
    ok_('た' != path[0].word)

def test_structured_perceptron_multiple_sentence():
    learner = graph.StructuredPerceptron()
    learner.train([(('a', 'o', 'i', 'o', 'a'),['あお', 'し', 'もさ']), (('a', 'o', 'o', 'a'), ['あ', 'と', 'と', 'さ'])], prefix_searcher, tone_list)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'i', 'o', 'a'))
    g.learner = learner
    path = g.search_shortest_path()
    eq_('あお', path[0].word)
    eq_('し', path[1].word)
    eq_('もさ', path[2].word)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'o', 'a'))
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
        for s, d in [(('a', 'o', 'i', 'o', 'a'),['あお', 'し', 'もさ']), (('a', 'o', 'o', 'a'), ['あ', 'と', 'と', 'さ'])]:
            yield (s, d)

    learner = graph.StructuredPerceptron()
    learner.train(iteratorWrapper(data), prefix_searcher, tone_list)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'i', 'o', 'a'))
    g.learner = learner
    path = g.search_shortest_path()
    eq_('あお', path[0].word)
    eq_('し', path[1].word)
    eq_('もさ', path[2].word)
    g = graph.Graph.construct_graph(prefix_searcher, tone_list, ('a', 'o', 'o', 'a'))
    g.learner = learner
    path = g.search_shortest_path()
    eq_('あ', path[0].word)
    eq_('と', path[1].word)
    eq_('と', path[2].word)
    eq_('さ', path[3].word)
