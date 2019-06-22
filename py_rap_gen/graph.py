# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Graph Shortes Path Solution."""
import sys
import heapq
import random
import numpy as np


UNKNOW_WORD = "<UNKNOWN>"


class SearchShortestPathError(Exception):
    """Shortest path search error"""
    pass


class Node(object):
    """Graph Node Object."""
    def __init__(self, start_pos, word):
        self.start_pos = start_pos
        self.word = word
        self.cost = 0
        self.prev = None

    def __eq__(self, other):
        return (
            self.start_pos == other.start_pos and
            self.word == other.word and
            self.cost == other.cost and
            self.prev == other.prev
        )

    def __hash__(self):
        return hash((
            self.start_pos,
            self.word,
            self.cost,
            self.prev))


class Path(object):
    """Graph Path Object."""
    def __init__(self):
        self.start_pos = -1
        self.words = []
        self.g_cost = 0
        self.f_cost = 0

    def __gt__(self, other):
        return True


class Graph(object):
    """Graph Object."""
    def __init__(self):
        self.nodes = []  # common endo position words list
        self.BOS = Node(0, "<BOS>")
        self.EOS = Node(-1, "<EOS>")
        self._learner = None

    @property
    def learner(self):
        return self._learner

    @learner.setter
    def learner(self, l):
        self._learner = l

    @classmethod
    def construct_graph(cls, prefix_searcher, string_list, string):
        """Construct convert graph.

        Args:
            prefix_searcher (TrieBase): trie data
            string_list (Hash[Tuple[String], List[String]]): string to string dictionary.
            string (Tuple[String]): target string.

        Return:
            graph (Graph): new graph object.
        """
        g = Graph()

        for _ in range(len(string) + 2):
            g.nodes.append([])
        g.nodes[0] = [g.BOS]
        g.EOS = Node(len(string), "<EOS>")
        g.nodes[len(string) + 1] = [g.EOS]

        for i in range(len(string)):
            for s in prefix_searcher.prefix_search(string[i:]):
                g.nodes[i + len(s)].extend([Node(i, str(w)) for w in string_list[s]])

        return g

    def _calculate_min_cost(self):
        """Calculate minimum node cost by viterbi algorithme."""
        N = len(self.nodes)

        for i in range(1, N):
            for node in self.nodes[i]:
                node.cost = sys.maxsize
                node_cost = self._learner.get_node_cost(node)
                for prev in self.nodes[node.start_pos]:
                    edge_cost = self._learner.get_edge_cost(prev, node)
                    cost = prev.cost + edge_cost + node_cost
                    if cost < node.cost:
                        node.cost = cost
                        node.prev = prev

    def search_nbest_path(self, N, beam_width=10):
        """Return graph n-bet path by A* algorithme.

        Args:
            N (Int): return path nums
            beam_width (Int): max next path size

        Return:
            paths (List[Path]): n-best short path node.
        """
        paths = []
        count = 0
        queue = []

        # Initialize queue
        eos = Path()
        eos.start_pos = self.EOS.start_pos
        eos.words = [self.EOS]
        heapq.heappush(queue, (eos.f_cost, eos))
        self._calculate_min_cost()

        # Search N-best paths by A* algorithme.
        while count != N and len(queue) != 0:
            path = heapq.heappop(queue)[1]
            if path.words[0] == self.BOS:
                # Add one of path to results
                paths.append(path.words[1:])
                count += 1
                continue

            nodes = self.nodes[path.start_pos]
            nodes = nodes if len(nodes) < beam_width else random.sample(nodes, beam_width)
            for prev in nodes:
                p = Path()
                edge_cost = self._learner.get_edge_cost(prev, path.words[0])
                node_cost = self._learner.get_node_cost(prev)
                p.g_cost = path.g_cost + edge_cost + node_cost
                p.f_cost = p.g_cost + prev.cost - node_cost
                p.words = [prev] + path.words
                p.start_pos = prev.start_pos
                heapq.heappush(queue, (p.f_cost, p))

        return paths

    def search_shortest_path(self):
        """Return graph shortest path.

        Return:
            path (List[Node]): node list constructs shortest path.
        """
        self._calculate_min_cost()
        node = self.EOS
        result = []
        while node != self.BOS:
            result.insert(0, node)
            node = node.prev
            if node is None:
                raise SearchShortestPathError()

        return result


class StructuredLearner(object):
    def __init__(self):
        self._N = 10000
        self._w = np.ones((self._N, ), dtype=np.float32) * 1000
        self._feature2index = {}
        self._index2feature = []

    @property
    def N(self):
        """Feature nums."""
        return self._N

    @N.setter
    def N(self, val):
        self._N = int(val)
        self._w = np.ones((self._N, ), dtype=np.float32) * 1000

    def construct_feature(self, features):
        """Construct feature dictionary.

        Args:
            features (List[String]): feature string list.
        """
        for f in features:
            if len(self._index2feature) < self._N:
                self._index2feature.append(f)
                self._feature2index[f] = len(self._index2feature) - 1

    def get_node_feature(self, node):
        """Return node feature.

        Args:
            node (Node): target node object.

        Return:
            feature (String): string represent features.
        """
        return node.word

    def get_edge_feature(self, prev, node):
        """Return edge feature.

        Args:
            prev (Node): previous node object.
            node (Node): target node object.

        Return:
            feature (String): string represent features.
        """
        return prev.word + '_' + node.word

    def get_node_cost(self, node):
        """Return node cost.

        Args:
            node (Node): target node object.

        Return:
            cost (Int): node cost value.
        """
        feature = self.get_node_feature(node)
        if feature not in self._feature2index:
            if len(self._index2feature) < self._N:
                self._index2feature.append(feature)
                self._feature2index[feature] = len(self._index2feature) - 1
            else:
                return 0

        return self._w[self._feature2index[feature]]

    def get_edge_cost(self, prev, node):
        """Return prev to node edge cost.

        Args:
            prev (Node): previous node object.
            node (Node): target node object.

        Return:
            cost (Int): edge cost value.
        """
        feature = self.get_edge_feature(prev, node)
        if feature not in self._feature2index:
            if len(self._index2feature) < self._N:
                self._index2feature.append(feature)
                self._feature2index[feature] = len(self._index2feature) - 1
            else:
                return 0

        return self._w[self._feature2index[feature]]

    def update_feature(self, feature, is_true):
        """Update feature.

        Args:
            feature (String): string represent features.
            is_true (bool): feature is correct or not.
        """
        updated_val = -1.0 if is_true else 1.0
        if feature in self._feature2index:
            self._w[self._feature2index[feature]] += updated_val
            if self._w[self._feature2index[feature]] < 0:
                self._w[self._feature2index[feature]] = 0

    def train(self, strings, golds):
        """Training learnier.

        Args:
            train_data (List[Tuple[Tuple[String], List[String]]]): trainning data construct target string and correct sentenece pairs.
        """
        pass


class StructuredPerceptron(StructuredLearner):
    def __init__(self):
        super().__init__()
        self._epochs = 1000
        self._vocabs = set()

    @property
    def epochs(self):
        """Training epoch nums."""
        return self._epochs

    @epochs.setter
    def epochs(self, val):
        self._epochs = val

    def get_node_feature(self, node):
        """Return node feature.

        Args:
            node (Node): target node object.
            vocabs (Set[String]): target vocabulary.

        Return:
            feature (String): string represent features.
        """
        if node.word in self._vocabs:
            return node.word
        else:
            return UNKNOW_WORD

    def get_edge_feature(self, prev, node):
        """Return edge feature.

        Args:
            prev (Node): previous node object.
            node (Node): target node object.

        Return:
            feature (String): string represent features.
        """
        if prev.word in self._vocabs:
            p = prev.word
        else:
            p = UNKNOW_WORD

        if node.word in self._vocabs:
            n = node.word
        else:
            n = UNKNOW_WORD

        return p + '_' + n

    def train(self, train_data, prefix_searcher, string_list):
        """Construct convert graph.

        Args:
            train_data (List[Tuple[Tuple[String], List[String]]]): trainning data construct target string and correct sentenece pairs.
            prefix_searcher (TrieBase): trie data
            string_list (Hash[Tuple[String], List[String]]): string to string dictionary.
        """
        vocabs = set()
        for v in string_list.values():
            vocabs |= set(v)
        self._vocabs = vocabs

        for v in self._vocabs:
            feature = self.get_node_feature(Node(-1, v))
            self._index2feature.append(feature)
            self._feature2index[feature] = len(self._index2feature) - 1

        for _ in range(self._epochs):
            for string, gold in train_data:
                g = Graph.construct_graph(prefix_searcher, string_list, string)
                g.learner = self
                try:
                    path = g.search_shortest_path()
                except SearchShortestPathError:
                    continue
                path = path[:-1]
                if [n.word for n in path] != gold:
                    for i in range(len(path)):
                        self.update_feature(self.get_node_feature(path[i]), False)
                        if i == 0:
                            self.update_feature(self.get_edge_feature(g.BOS, path[i]), False)
                        elif i == len(path) - 1:
                            self.update_feature(self.get_edge_feature(path[i], g.EOS), False)
                        else:
                            self.update_feature(self.get_edge_feature(path[i-1], path[i]), False)

                    for i in range(len(gold)):
                        self.update_feature(self.get_node_feature(Node(-1, gold[i])), True)
                        if i == 0:
                            self.update_feature(self.get_edge_feature(g.BOS, Node(-1, gold[i])), True)
                        elif i == len(gold) - 1:
                            self.update_feature(self.get_edge_feature(Node(-1, gold[i]), g.EOS), True)
                        else:
                            self.update_feature(self.get_edge_feature(Node(-1, gold[i-1]), Node(-1, gold[i])), True)
