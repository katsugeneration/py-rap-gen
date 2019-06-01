# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Graph Shortes Path Solution."""
import sys
import numpy as np


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
            string_list (Hash[String, List[String]]): string to string dictionary.
            string (String): target string.

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
                g.nodes[i + len(s)].extend([Node(i, w) for w in string_list[s]])

        return g

    def get_node_cost(self, node):
        """Return node cost.

        Args:
            node (Node): target node object.

        Return:
            cost (Int): node cost value.
        """
        return self._learner.get_node_cost(node)

    def get_edge_cost(self, prev, node):
        """Return prev to node edge cost.

        Args:
            prev (Node): previous node object.
            node (Node): target node object.

        Return:
            cost (Int): edge cost value.
        """
        return self._learner.get_edge_cost(prev, node)

    def search_shortest_path(self):
        """Return graph shortest path.

        Return:
            path (List[Node]): node list constructs shortest path.
        """
        N = len(self.nodes)

        # cost calculation (viterbi algorithm)
        for i in range(1, N):
            for node in self.nodes[i]:
                node.cost = sys.maxsize
                node_cost = self.get_node_cost(node)
                for prev in self.nodes[node.start_pos]:
                    edge_cost = self.get_edge_cost(prev, node)
                    cost = prev.cost + edge_cost + node_cost
                    if cost < node.cost:
                        node.cost = cost
                        node.prev = prev

        # search shortest path
        node = self.EOS
        result = []
        while node != self.BOS:
            result.insert(0, node)
            node = node.prev

        return result


class StructuredLearner(object):
    def __init__(self):
        self._N = 10000
        self._w = np.ones((self._N, ), dtype=np.int32) * 1000
        self._feature2index = {}
        self._index2feature = []

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
        return self.get_node_feature(prev) + '_' + self.get_node_feature(node)

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
            strings (List[String]): observable values.
            golds (List[List[String]]): correct converted suqences.
        """
        pass


class StructuredPerceptron(StructuredLearner):
    def __init__(self):
        super().__init__()
        self._epoch = 1000

    def train(self, strings, golds, prefix_searcher, string_list):
        """Construct convert graph.

        Args:
            strings (List[String]): target string list.
            golds (List[List[String]]): correct senteneces lists.
            prefix_searcher (TrieBase): trie data
            string_list (Hash[String, List[String]]): string to string dictionary.
        """
        for _ in range(self._epoch):
            for string, gold in zip(strings, golds):
                g = Graph.construct_graph(prefix_searcher, string_list, string)
                g.learner = self
                path = g.search_shortest_path()
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
